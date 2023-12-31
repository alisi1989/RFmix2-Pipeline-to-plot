#!/usr/bin/env python3
#Autors Alessandro Lisi & Michael C. Campbell
#be sure to priorly install librsvg (brew install rsvg) or for Linux machine "https://manpages.ubuntu.com/manpages/trusty/man1/rsvg-convert.1.html"

#use python LAP.py --help to see the option

import argparse
import xml.etree.ElementTree as ET
import os
import subprocess

def insert_colored_regions(svg_file, bed_file, output_file, individual_name, ancestries):
    # Definisci manualmente le coordinate dei cromosomi
    chromosome_coordinates = {
        'chromosome1_hap1': {'x': 225.000, 'y': 103.20, 'width': 20.5, 'height': 666.300},
        'chromosome1_hap2': {'x': 246.100, 'y': 103.20, 'width': 20, 'height': 666.300},
        'chromosome2_hap1': {'x': 288.300, 'y': 121.300, 'width': 20, 'height': 648.200},
        'chromosome2_hap2': {'x': 309.200, 'y': 121.300, 'width': 20, 'height': 648.200},
        'chromosome3_hap1': {'x': 351.000, 'y': 238.600, 'width': 20, 'height': 530.900},
        'chromosome3_hap2': {'x': 372.000, 'y': 238.600, 'width': 20, 'height': 530.900},
        'chromosome4_hap1': {'x': 413.800, 'y': 260.200, 'width': 20, 'height': 509.300},
        'chromosome4_hap2': {'x': 434.600, 'y': 260.200, 'width': 20, 'height': 509.300},
        'chromosome5_hap1': {'x': 476.600, 'y': 283.300, 'width': 20, 'height': 486.200},
        'chromosome5_hap2': {'x': 497.500, 'y': 283.300, 'width': 20, 'height': 486.200},
        'chromosome6_hap1': {'x': 539.400, 'y': 312.000, 'width': 20, 'height': 457.500},
        'chromosome6_hap2': {'x': 560.300, 'y': 312.000, 'width': 20, 'height': 457.500},
        'chromosome7_hap1': {'x': 602.200, 'y': 342.600, 'width': 20, 'height': 426.900},
        'chromosome7_hap2': {'x': 623.100, 'y': 342.600, 'width': 20, 'height': 426.900},
        'chromosome8_hap1': {'x': 664.900, 'y': 380.600, 'width': 20, 'height': 388.900},
        'chromosome8_hap2': {'x': 685.800, 'y': 380.600, 'width': 20, 'height': 388.900},
        'chromosome9_hap1': {'x': 727.500, 'y': 398.600, 'width': 20, 'height': 370.900},
        'chromosome9_hap2': {'x': 748.400, 'y': 398.600, 'width': 20, 'height': 370.900},
        'chromosome10_hap1': {'x': 790.500, 'y': 410.900, 'width': 20, 'height': 358.600},
        'chromosome10_hap2': {'x': 811.400, 'y': 410.900, 'width': 20, 'height': 358.600},
        'chromosome11_hap1': {'x': 853.300, 'y': 407.500, 'width': 20, 'height': 362.000},
        'chromosome11_hap2': {'x': 874.200, 'y': 407.500, 'width': 20, 'height': 362.00},
        'chromosome12_hap1': {'x': 916.000, 'y': 412.300, 'width': 20, 'height': 357.200},
        'chromosome12_hap2': {'x': 937.000, 'y': 412.300, 'width': 20, 'height': 357.200},
        'chromosome13_hap1': {'x': 978.600, 'y': 462.800, 'width': 20, 'height': 306.700},
        'chromosome13_hap2': {'x': 999.500, 'y': 462.800, 'width': 20, 'height': 306.700},
        'chromosome14_hap1': {'x': 1041.600, 'y': 482.400, 'width': 20, 'height': 287.100},
        'chromosome14_hap2': {'x': 1062.500, 'y': 482.400, 'width': 20, 'height': 287.100},
        'chromosome15_hap1': {'x': 1104.600, 'y': 495.900, 'width': 20, 'height': 273.600},
        'chromosome15_hap2': {'x': 1125.600, 'y': 495.900, 'width': 20, 'height': 273.600},
        'chromosome16_hap1': {'x': 1166.600, 'y': 527.100, 'width': 20, 'height': 242.400},
        'chromosome16_hap2': {'x': 1187.600, 'y': 527.100, 'width': 20, 'height': 242.400},
        'chromosome17_hap1': {'x': 1229.900, 'y': 546.000, 'width': 20, 'height': 223.500},
        'chromosome17_hap2': {'x': 1250.800, 'y': 546.000, 'width': 20, 'height': 223.500},
        'chromosome18_hap1': {'x': 1292.500, 'y': 553.700, 'width': 20, 'height': 215.800},
        'chromosome18_hap2': {'x': 1313.400, 'y': 553.700, 'width': 20, 'height': 215.800},
        'chromosome19_hap1': {'x': 1355.400, 'y': 611.800, 'width': 20, 'height': 157.700},
        'chromosome19_hap2': {'x': 1376.400, 'y': 611.800, 'width': 20, 'height': 157.700},
        'chromosome20_hap1': {'x': 1418.200, 'y': 596.200, 'width': 20, 'height': 173.300},
        'chromosome20_hap2': {'x': 1439.200, 'y': 596.200, 'width': 20, 'height': 173.300},
        'chromosome21_hap1': {'x': 1481.000, 'y': 643.300, 'width': 20, 'height': 125.900},
        'chromosome21_hap2': {'x': 1501.900, 'y': 643.300, 'width': 20, 'height': 125.900},
        'chromosome22_hap1': {'x': 1543.800, 'y': 632.700, 'width': 20, 'height': 136.800},
        'chromosome22_hap2': {'x': 1564.700, 'y': 632.700, 'width': 20, 'height': 136.800},
        
    }

    # Definisci manualmente le lunghezze dei cromosomi
    chromosome_lengths = [249250621, 242193529, 198295559, 190214555, 181538259, 170805979, 159345973, 145138636, 138394717, 133797422, 135086622, 133275309, 114364328, 107043718, 101991189, 90338345, 83257441, 80373285, 58617616, 64444167, 46709983, 50818468]

    # Parsing del file SVG originale
    original_svg_tree = ET.parse(svg_file)
    original_svg_root = original_svg_tree.getroot()

    # Aggiungi solo il nome dell'individuo come titolo nel file SVG
    title_element = ET.Element('text', {'x': "800", 'y': "30", 'fill': "black", 'font-size': "32"})
    title_element.text = individual_name
    original_svg_root.insert(0, title_element)  # Inserisci il titolo all'inizio del documento

    # Crea una leggenda se gli ancestries sono specificati
    if ancestries:
        y_offset = 40  # Inizia a disegnare la leggenda da questa coordinata y
        for ancestry, (name, color) in ancestries.items():
            # Rettangolo colorato
            rect_element = ET.Element('rect', {'x': "1450", 'y': str(y_offset), 'width': "25", 'height': "15", 'fill': color})
            original_svg_root.insert(0, rect_element)

            # Testo dell'ancestria
            text_element = ET.Element('text', {'x': "1480", 'y': str(y_offset + 15), 'fill': "black", 'font-size': "22"})
            text_element.text = name
            original_svg_root.insert(0, text_element)

            y_offset += 30  # Aggiorna la coordinata y per la prossima voce della leggenda
            
    rectangle_elements = []
    line_elements = []
    
    # Estrai le regioni dal file BED
    with open(bed_file, 'r') as bed:
        for line in bed:
            parts = line.strip().split('\t')
            if len(parts) < 6:
                continue

            chromosome, start, end, line_type, color, haplotype = parts[:6]
            chromosome = int(chromosome)
            start, end, haplotype = int(start), int(end), int(haplotype)

            chromosome_id = f'chromosome{chromosome}_hap{haplotype}'
            if chromosome_id in chromosome_coordinates:
                chromosome_data = chromosome_coordinates[chromosome_id]
                chromosome_length = chromosome_lengths[chromosome - 1]

                x = chromosome_data['x']
                width = chromosome_data['width']
                start_y = chromosome_data['y'] + (start / chromosome_length) * chromosome_data['height']
                end_y = chromosome_data['y'] + (end / chromosome_length) * chromosome_data['height']

                if line_type == 'geom_line':
                    offset=15
                    line_element_start = ET.Element('line', {
                        'x1': str(x - offset),
                        'y1': str(start_y),
                        'x2': str(x + width + offset),
                        'y2': str(start_y),
                        'stroke': color,
                        'stroke-width': '3',
                        'stroke-dasharray': '10'
                    })
                    line_element_end = ET.Element('line', {
                        'x1': str(x - offset),
                        'y1': str(end_y),
                        'x2': str(x + width + offset),
                        'y2': str(end_y),
                        'stroke': color,
                        'stroke-width': '3',
                        'stroke-dasharray': '10'
                    })
                    original_svg_root.insert(0, line_element_start)
                    original_svg_root.insert(0, line_element_end)
                else:
                    rect_element = ET.Element('rect', {
                        'x': str(x),
                        'y': str(start_y),
                        'width': str(width),
                        'height': str(end_y - start_y),
                        'fill': color
                    })
                    rectangle_elements.append(rect_element)
    for elem in rectangle_elements + line_elements:
        original_svg_root.insert(0, elem)

    # Salva il risultato modificato nel file SVG
    original_svg_tree.write(output_file)

    # Chiama rsvg-convert per convertire il file SVG in un formato diverso (PDF)
    output_format = "pdf"  # Modifica a seconda delle necessità
    input_svg = output_file
    output_file_pdf = os.path.splitext(output_file)[0] + f'.{output_format}'
    subprocess.run(["rsvg-convert", "-f", output_format, "-o", output_file_pdf, input_svg])
    print(f"File converted to {output_format}: {output_file_pdf}")

def parse_svg_filename(filename):
    if not filename.endswith('.svg'):
        filename += '.svg'
    return filename

def main():
    parser = argparse.ArgumentParser(description='Insert colored regions from a BED file into an SVG file.')
    parser.add_argument('-B', type=parse_svg_filename, default='hg38', help='Input build38 "hg38" file without extension')
    parser.add_argument('-I', type=str, required=True, help='Input BED file')
    parser.add_argument('-O', type=str, required=True, help='Output SVG file')
    parser.add_argument('--ancestry0', nargs=2, help='Name and color for ancestry0, e.g., --ancestry0 Africa #0000ff')
    parser.add_argument('--ancestry1', nargs=2, help='Name and color for ancestry1, e.g., --ancestry1 Europe #850b39')
    parser.add_argument('--ancestry2', nargs=2, help='Name and color for ancestry2, e.g., --ancestry2 Middle_East #F4A500')
    args = parser.parse_args()

    # Mappa degli ancestries
    ancestries = {}
    if args.ancestry0:
        ancestries['ancestry0'] = (args.ancestry0[0], args.ancestry0[1])
    if args.ancestry1:
        ancestries['ancestry1'] = (args.ancestry1[0], args.ancestry1[1])
    if args.ancestry2:
        ancestries['ancestry2'] = (args.ancestry2[0], args.ancestry2[1])

    # Estrai il nome dell'individuo dal file BED
    individual_name = os.path.basename(args.I).split('.')[0]

    insert_colored_regions(args.B, args.I, args.O, individual_name, ancestries)

if __name__ == "__main__":
    main()
