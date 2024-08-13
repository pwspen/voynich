"""IVTFF
Contains helpful functions to work with Rene Zandbergen's IVTFF file format
Learn more here: https://www.voynich.nu/software/ivtt/IVTFF_format.pdf
"""

import re

# defining some useful regular expressions
RE_LOCUS_ID = r'<(f\d+[vr])\.\d+,[@+*\-=&~]\w+(;T)?>'
RE_INLINE_COMMENT = r'<.*?>'
RE_HIGH_ASCII = r'@(\d{3});'
RE_UNCERTAIN_READING = r'\[(.*?)\]'

def parse_metadata(text):
    pattern = r'<f.{1,10}>\s+<!\s+(?:(?:\$([QPFBILHCX])=([^>\s]+))[\s>]*)*>'
    match = re.match(pattern, text)
    if match:
        result = {}
       
        # Extract folio
        folio_match = re.match(r'<(f.{1,10})>', text)
        if folio_match:
            result['page'] = folio_match.group(1)
        else:
            raise ValueError("Variable header matched but no folio found")
       
        # Create a sub-dictionary for page_info
        result['page_info'] = {}
       
        # Variable name mapping
        var_mapping = {
            'Q': 'quire',
            'P': 'pagenum_in_quire',
            'F': 'folionum_in_quire',
            'B': 'bifolionum_in_quire',
            'I': 'illust_type',
            'L': 'currier_language',
            'H': 'hand',
            'C': 'currier_hand',
            'X': 'extr_writing'
        }
       
        # Illustration type mapping
        illust_type_mapping = {
            'A': 'astronomical',
            'B': 'biological',
            'C': 'cosmological',
            'H': 'herbal',
            'P': 'pharmaceutical',
            'S': 'stars_only',
            'T': 'text_only',
            'Z': 'zodiac'
        }
        
        # Extra writing mapping
        extr_writing_mapping = {
            'C': 'color_annotation',
            'M': 'month',
            'O': 'other',
            'S': 'char_or_num_seq'
        }
       
        # Extract all variables and add them to page_info
        for var, value in re.findall(r'\$([QPFBILHCX])=([^>\s]+)', text):
            if var == 'I':
                result['page_info'][var_mapping[var]] = illust_type_mapping.get(value, value)
            elif var == 'X':
                result['page_info'][var_mapping[var]] = extr_writing_mapping.get(value, value)
            else:
                result['page_info'][var_mapping[var]] = value
       
        return result
    else:
        return None

def parse_transliteration(text: str) -> dict:
    """
    Parses the given transliteration text in IVTFF format into a dict
    where key=page name (ex. 'f1r'), and value=the parsed text
    """

    # extracting non-empty lines from the text
    lines = list(filter(lambda x: len(x) > 0, text.split('\n')))

    out = {}

    for line in lines:
        # throwing away comments
        if line[0] == '#':
            continue
        # we only care about lines with loci
        match = re.match(RE_LOCUS_ID, line)
        if match is None:
            meta = parse_metadata(line)
            if meta:
                print(meta)
                out[meta['page']] = {}
                out[meta['page']]['page_info'] = meta['page_info']
                out[meta['page']]['text'] = ''
            continue

        # first removing unwanted characters & comments, then adding spaces between words
        trans_text = re.sub(r'[ {}?]', '', line[len(match.group(0)):])
        trans_text = re.sub(RE_INLINE_COMMENT, '', trans_text)
        trans_text = re.sub(r'[.,]', ' ', trans_text)

        # replacing high-ascii identifiers with the actual high-ascii character
        for mat in re.finditer(RE_HIGH_ASCII, trans_text):
            trans_text = trans_text.replace(mat.group(0), chr(int(mat.group(1))))

        # replacing uncertain translations with the first option
        for mat in re.finditer(RE_UNCERTAIN_READING, trans_text):
            options = mat.group(1).split(':')

            # sometimes to denote two possible one-character readings we use [ab] instead of [a:b]
            # so in this case we simply return the first character
            if len(options) < 2:
                trans_text = trans_text.replace(mat.group(0), mat.group(1)[0])
            else:
                trans_text = trans_text.replace(mat.group(0), options[0])

        # adding this text to the current page's contents
        page = match.group(1)
        # each locus should be separated by a new line to indicate it as a unique locus
        out[page]['text'] = out.get(page, '')['text'] + trans_text + '\n'
    return out
