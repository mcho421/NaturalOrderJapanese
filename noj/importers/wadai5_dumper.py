#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import string
import sys

import eb
from wadai5_gaiji import WADAI5_GAIJI

class Wadai5Dumper(object):
    """Dump Kenkyusha 5th EPWING Dictionary into a file
    Sanitises the output for re-importing with Importer"""
    def __init__(self, dictdir, outfile):
        super(Wadai5Dumper, self).__init__()
        self.dictdir = dictdir
        self.outfile = outfile
        self.first_pos = (108260, 1606) # first entry pos
        self.last_pos = (159979, 1882)  # last pos with useful info
        # (159979, 1944) is first position with useless info
        # (107887, 872) is the foreword

        eb.eb_initialize_library()
        self.book     = eb.EB_Book()
        self.appendix = eb.EB_Appendix() 
        self.hookset  = eb.EB_Hookset()
        self.gaiji    = WADAI5_GAIJI

        eb.eb_set_hooks(self.hookset, (
            (eb.EB_HOOK_NARROW_FONT, self.hook_font),
            (eb.EB_HOOK_WIDE_FONT,   self.hook_font),
            (eb.EB_HOOK_BEGIN_REFERENCE, self.hook_begin_reference),
            (eb.EB_HOOK_END_REFERENCE, self.hook_end_reference)))

        try:
            eb.eb_bind(self.book, self.dictdir)
        except eb.EBError, (error, message):
            code = eb.eb_error_string(error)
            sys.stderr.write("Error: %s: %s\n" % (code, message))
            sys.exit(1)
        eb.eb_set_subbook(self.book, 0)

    def hook_font(self, book, appendix, container, code, argv):
        if (code, argv[0]) in self.gaiji:
            replacement = "{{0x{}}}".format(
                    self.gaiji[(code, argv[0])].encode('hex'))
        else:
            replacement = '#'
        eb.eb_write_text_string(book, replacement)
        return eb.EB_SUCCESS

    def hook_begin_reference(self, book, appendix, container, code, argv):
         eb.eb_write_text_string(book, "<LINK>")
         return eb.EB_SUCCESS

    def hook_end_reference(self, book, appendix, container, code, argv):
        eb.eb_write_text_string(book, "</LINK[{:d}:{:d}]>".format(
            argv[1], argv[2]))
        return eb.EB_SUCCESS

    def get_content(self):
        buffer = []
        while 1:
            data = eb.eb_read_text(self.book, self.appendix, 
                    self.hookset, None)
            if not data:
                break
            buffer.append(data)
        data = string.join(buffer, "")
        return data

    def replace_gaiji_hex_sub_helper(self, match):
        """Returns the utf-8 gaiji given the utf-8 hex code
        for the gaiji"""
        return match.group(1).decode('hex')

    def replace_gaiji_hex(self, utf8_string):
        """Given a UTF-8 string, replace all instances of gaiji
        hexadecimal tags to appropriate UTF-8 gaiji. Returns 
        a new string with all gaiji hex tags replace with gaiji"""
        #print re.findall("{0x[0-9a-f]+}", utf8_string)
        return re.sub(r'{0x([0-9a-f]+)}', 
                self.replace_gaiji_hex_sub_helper, utf8_string)

    def dump_generator(self):
        fh = open(self.outfile, "w")
        pos = self.first_pos
        eb.eb_seek_text(self.book, pos)
        while pos <= self.last_pos:
            content = self.get_content()
            utf8_content = content.decode(
                'euc-jp', errors='ignore').encode('utf-8',errors='ignore')
            # print self.replace_gaiji_hex(utf8_content)
            fh.write(self.replace_gaiji_hex(utf8_content))
            pos = eb.eb_tell_text(self.book)
            # print(pos)
            eb.eb_seek_text(self.book, (pos[0], pos[1]+2))
            yield pos[0] - self.first_pos[0]
        fh.close()

    def get_num_pos(self):
        return self.last_pos[0] - self.first_pos[0]
        
def main():
    dictdir = 'C:\\Users\\Mathew\\ISO\\[EPWING] KenKyuSha 5th'
    outfile = 'kendump.txt'
    dumper = Wadai5Dumper(dictdir, outfile)
    num_pos = dumper.get_num_pos()

    import progressbar as pb
    widgets = ['Dumping: ', pb.Percentage(), ' ', pb.Bar(),
               ' ', pb.Timer(), ' ']
    pbar = pb.ProgressBar(widgets=widgets, maxval=num_pos).start()

    for i in dumper.dump_generator(:)
        pbar.update(i)
    pbar.finish()

if __name__ == '__main__':
    main()
