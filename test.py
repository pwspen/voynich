import re

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
            'S': 'char_or_num_seq',
            'V': 'various'
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

# Test the function
test_lines = ['<fRos>     <! $Q=N $P=D      $B=1 $I=C $L=B $H=4 $C=3>',
              '<f85r2.24,@Cc>    <!09:30>okees.ochar.oted[o:a]r.ochedy.otody.olchedy.oteedo.ar.or.airol.otees.ar.aram',
              '<f17r>     <! $Q=C $P=A $F=a $B=1 $I=H $L=A $H=1 $C=1 $X=O>',
              '<f20r>     <! $Q=C $P=G $F=d $B=4 $I=P $L=A $H=1 $C=1 $X=C>',
              '<f1r>      <! $Q=A $P=A $F=a $B=1 $I=T $L=A $H=1 $C=1 $X=V>']

for l in test_lines:
    print(parse_metadata(l))