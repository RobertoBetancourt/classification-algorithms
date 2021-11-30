RELATION_BASE_STR = "@relation '{relation_name}'\n"
ATTRIBUTE_BASE_STR = "@attribute Text string\n"
ATTRIBUTE_CLASS_BASE_STR = "@attribute class-att {0,1}\n"
DATA_BASE_STR = "@data\n"

def open_file_read(location):
  try:
    file_iterator = open(location)
    return file_iterator
  except Exception as error:
    print ('No se pudo leer el archivo', error.message)
    return None

def open_file_append(location):
  try:
    file_iterator = open(location, "a")
    return file_iterator
  except Exception as error:
    print('No se pudo leer el archivo', error.message)
    return None


def parse_header(file_to_write_pointer, relation_name):
  try:
    file_to_write_pointer.write(RELATION_BASE_STR.format(relation_name=relation_name))
    file_to_write_pointer.write(ATTRIBUTE_BASE_STR)
    file_to_write_pointer.write(ATTRIBUTE_CLASS_BASE_STR)
    file_to_write_pointer.write(DATA_BASE_STR)
  except Exception as error:
    print('No se pudo agregar el encabezado', error.message)
    return None


def clean_string(original_string):
  return original_string.lower().replace("'", "")

def get_class(original_string):
  if (len(original_string) > 1):
    return original_string[-2]
  else:
    return ""

def remove_class(original_string):
  if (len(original_string) > 1):
    return original_string[:-3]
  else:
    return original_string

def assemble_string_to_write(class_from_string, string_without_class):
  return f"'{string_without_class}',{class_from_string}\n"

def parse_body(file_to_read_pointer, file_to_write_pointer):
  for line in file_to_read_pointer:
    clean_line = clean_string(line)
    class_from_string = get_class(clean_line)
    string_without_class = remove_class(clean_line)
    string_to_write = assemble_string_to_write(class_from_string=class_from_string, string_without_class=string_without_class)
    file_to_write_pointer.write(string_to_write)


def parse_txt_to_arff(txt_location, arff_location):
  file_to_read_pointer = open_file_read(txt_location)
  file_to_write_pointer = open_file_append(arff_location)

  parse_header(file_to_write_pointer=file_to_write_pointer, relation_name="Amazon")
  parse_body(file_to_read_pointer=file_to_read_pointer, file_to_write_pointer=file_to_write_pointer)

  file_to_read_pointer.close()
  file_to_write_pointer.close()

if __name__ == '__main__':
  parse_txt_to_arff(txt_location="./amazon_cells_labelled.txt", arff_location="./amazon.arff")

