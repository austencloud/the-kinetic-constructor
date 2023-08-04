import os
from lxml import etree

def set_svg_id(directory):
    # iterate over files in the directory
    for filename in os.listdir(directory):
        # check if the file is an SVG file
        if filename.endswith(".svg"):
            # parse the SVG file
            parser = etree.XMLParser(remove_blank_text=True)
            tree = etree.parse(os.path.join(directory, filename), parser)
            root = tree.getroot()

            # find the first 'path' element
            path_elem = root.find('.//{*}path')
            if path_elem is not None:
                # get a copy of existing attributes
                attrs = path_elem.attrib

                # set the 'id' attribute
                attrs['id'] = filename[:-4]  # remove the '.svg' from the filename

                # create a new attribute dictionary with 'id' first
                new_attrs = {'id': attrs.pop('id')}
                new_attrs.update(attrs)

                # update the 'path' element's attributes
                path_elem.attrib.clear()
                path_elem.attrib.update(new_attrs)

            # write the changes back to the file
            tree.write(os.path.join(directory, filename), pretty_print=True)

# usage
set_svg_id('images/arrows')
