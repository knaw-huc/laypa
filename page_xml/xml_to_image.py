import argparse
from pathlib import Path
import sys
import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.joinpath("..")))
from page_xml.xmlPAGE import PageData
from page_xml.xml_regions import XMLRegions
from typing import Optional


def get_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(parents=[XMLImage.get_parser()],
        description="Code to turn an xml file into an array")
    io_args = parser.add_argument_group("IO")
    io_args.add_argument("-i", "--input", help="Input file",
                        required=True, type=str)
    io_args.add_argument(
        "-o", "--output", help="Output file", required=True, type=str)
    
    

    args = parser.parse_args()
    return args


class XMLImage(XMLRegions):
    def __init__(self, mode: str, 
                 line_width: Optional[int] = None, 
                 line_color: Optional[int] = None, 
                 regions: Optional[list[str]] = None, 
                 merge_regions: Optional[list[str]] = None, 
                 region_type: Optional[list[str]] = None) -> None:
        super().__init__(mode, line_width, line_color, regions, merge_regions, region_type)

    def run(self, xml_path: Path, image_shape=None) -> np.ndarray:
        gt_data = PageData(xml_path)
        gt_data.parse()

        if image_shape is None:
            image_shape = gt_data.get_size()[::-1]

        if self.mode == "baseline":
            baseline_mask = gt_data.build_baseline_mask(image_shape,
                                                        color=self.line_color,
                                                        line_width=self.line_width)
            mask = baseline_mask
        elif self.mode == "region":
            region_mask = gt_data.build_mask(image_shape,
                                             set(self.region_types.values()),
                                             self.region_classes)
            mask = region_mask
        else:
            raise NotImplementedError

        return mask



if __name__ == "__main__":
    args = get_arguments()
    XMLImage(
        mode=args.mode,
        line_width=args.line_width,
        line_color=args.line_color,
        regions=args.regions,
        merge_regions=args.merge_regions,
        region_type=args.region_type
    )

    input_path = Path(args.input)
    output_path = Path(args.output)
    
    
    
    