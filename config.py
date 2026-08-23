"""
Configuration file containing strict constants, delivery format headers (252 fields),
placeholders, taxonomy keywords, UOM maps, and rule-based constants.
"""

# Section 3: Exact 252 Delivery Format Headers in verbatim order
DELIVERY_FORMAT_HEADERS = [
    "MFR URL", "Ref URL 1", "Ref URL 2", "Ref URL 3", "Ref URL 4", "Ref URL 5",
    "PART_NUMBER", "Dept", "Class", "Fine", "SKU - MY_PART_NUMBER", "Mfg_Part_Num",
    "Part_Desc", "E1_Brand", "Unilog_Brand", "DIB_Brand", "Part_Manuf",
    "MANUFACTURER_NAME", "BRAND_NAME", "TRADE_NAME", "MANUFACTURER_PART_NUMBER",
    "ALTERNATE_PART_NUMBER", "Classpath", "MOBILE_DESC", "INVOICE_DESC",
    "SHORT_DESC", "LONG_DESC1", "RETAIL_DESC", "MARKETING_DESCRIPTION",
    "ITEM_FEATURES_1", "ITEM_FEATURES_2", "ITEM_FEATURES_3", "ITEM_FEATURES_4",
    "ITEM_FEATURES_5", "ITEM_FEATURES_6", "ITEM_FEATURES_7", "ITEM_FEATURES_8",
    "ITEM_FEATURES_9", "ITEM_FEATURES_10", "ITEM_FEATURES_11", "ITEM_FEATURES_12",
    "ITEM_FEATURES_13", "ITEM_FEATURES_14", "ITEM_FEATURES_15", "ITEM_FEATURES_16",
    "ITEM_FEATURES_17", "ITEM_FEATURES_18", "ITEM_FEATURES_19", "ITEM_FEATURES_20",
    "With", "Standard/Approvals", "Prop 65", "Application", "Includes", "Product Name",
    "ATTRIBUTE_LABEL 1", "ATTRIBUTE_VALUE 1", "ATTRIBUTE_UOM 1",
    "ATTRIBUTE_LABEL 2", "ATTRIBUTE_VALUE 2", "ATTRIBUTE_UOM 2",
    "ATTRIBUTE_LABEL 3", "ATTRIBUTE_VALUE 3", "ATTRIBUTE_UOM 3",
    "ATTRIBUTE_LABEL 4", "ATTRIBUTE_VALUE 4", "ATTRIBUTE_UOM 4",
    "ATTRIBUTE_LABEL 5", "ATTRIBUTE_VALUE 5", "ATTRIBUTE_UOM 5",
    "ATTRIBUTE_LABEL 6", "ATTRIBUTE_VALUE 6", "ATTRIBUTE_UOM 6",
    "ATTRIBUTE_LABEL 7", "ATTRIBUTE_VALUE 7", "ATTRIBUTE_UOM 7",
    "ATTRIBUTE_LABEL 8", "ATTRIBUTE_VALUE 8", "ATTRIBUTE_UOM 8",
    "ATTRIBUTE_LABEL 9", "ATTRIBUTE_VALUE 9", "ATTRIBUTE_UOM 9",
    "ATTRIBUTE_LABEL 10", "ATTRIBUTE_VALUE 10", "ATTRIBUTE_UOM 10",
    "ATTRIBUTE_LABEL 11", "ATTRIBUTE_VALUE 11", "ATTRIBUTE_UOM 11",
    "ATTRIBUTE_LABEL 12", "ATTRIBUTE_VALUE 12", "ATTRIBUTE_UOM 12",
    "ATTRIBUTE_LABEL 13", "ATTRIBUTE_VALUE 13", "ATTRIBUTE_UOM 13",
    "ATTRIBUTE_LABEL 14", "ATTRIBUTE_VALUE 14", "ATTRIBUTE_UOM 14",
    "ATTRIBUTE_LABEL 15", "ATTRIBUTE_VALUE 15", "ATTRIBUTE_UOM 15",
    "ATTRIBUTE_LABEL 16", "ATTRIBUTE_VALUE 16", "ATTRIBUTE_UOM 16",
    "ATTRIBUTE_LABEL 17", "ATTRIBUTE_VALUE 17", "ATTRIBUTE_UOM 17",
    "ATTRIBUTE_LABEL 18", "ATTRIBUTE_VALUE 18", "ATTRIBUTE_UOM 18",
    "ATTRIBUTE_LABEL 19", "ATTRIBUTE_VALUE 19", "ATTRIBUTE_UOM 19",
    "ATTRIBUTE_LABEL 20", "ATTRIBUTE_VALUE 20", "ATTRIBUTE_UOM 20",
    "ATTRIBUTE_LABEL 21", "ATTRIBUTE_VALUE 21", "ATTRIBUTE_UOM 21",
    "ATTRIBUTE_LABEL 22", "ATTRIBUTE_VALUE 22", "ATTRIBUTE_UOM 22",
    "ATTRIBUTE_LABEL 23", "ATTRIBUTE_VALUE 23", "ATTRIBUTE_UOM 23",
    "ATTRIBUTE_LABEL 24", "ATTRIBUTE_VALUE 24", "ATTRIBUTE_UOM 24",
    "ATTRIBUTE_LABEL 25", "ATTRIBUTE_VALUE 25", "ATTRIBUTE_UOM 25",
    "ATTRIBUTE_LABEL 26", "ATTRIBUTE_VALUE 26", "ATTRIBUTE_UOM 26",
    "ATTRIBUTE_LABEL 27", "ATTRIBUTE_VALUE 27", "ATTRIBUTE_UOM 27",
    "ATTRIBUTE_LABEL 28", "ATTRIBUTE_VALUE 28", "ATTRIBUTE_UOM 28",
    "ATTRIBUTE_LABEL 29", "ATTRIBUTE_VALUE 29", "ATTRIBUTE_UOM 29",
    "ATTRIBUTE_LABEL 30", "ATTRIBUTE_VALUE 30", "ATTRIBUTE_UOM 30",
    "ATTRIBUTE_LABEL 31", "ATTRIBUTE_VALUE 31", "ATTRIBUTE_UOM 31",
    "ATTRIBUTE_LABEL 32", "ATTRIBUTE_VALUE 32", "ATTRIBUTE_UOM 32",
    "ATTRIBUTE_LABEL 33", "ATTRIBUTE_VALUE 33", "ATTRIBUTE_UOM 33",
    "ATTRIBUTE_LABEL 34", "ATTRIBUTE_VALUE 34", "ATTRIBUTE_UOM 34",
    "ATTRIBUTE_LABEL 35", "ATTRIBUTE_VALUE 35", "ATTRIBUTE_UOM 35",
    "ATTRIBUTE_LABEL 36", "ATTRIBUTE_VALUE 36", "ATTRIBUTE_UOM 36",
    "ATTRIBUTE_LABEL 37", "ATTRIBUTE_VALUE 37", "ATTRIBUTE_UOM 37",
    "ATTRIBUTE_LABEL 38", "ATTRIBUTE_VALUE 38", "ATTRIBUTE_UOM 38",
    "ATTRIBUTE_LABEL 39", "ATTRIBUTE_VALUE 39", "ATTRIBUTE_UOM 39",
    "ATTRIBUTE_LABEL 40", "ATTRIBUTE_VALUE 40", "ATTRIBUTE_UOM 40",
    "ATTRIBUTE_LABEL 41", "ATTRIBUTE_VALUE 41", "ATTRIBUTE_UOM 41",
    "ATTRIBUTE_LABEL 42", "ATTRIBUTE_VALUE 42", "ATTRIBUTE_UOM 42",
    "ATTRIBUTE_LABEL 43", "ATTRIBUTE_VALUE 43", "ATTRIBUTE_UOM 43",
    "ATTRIBUTE_LABEL 44", "ATTRIBUTE_VALUE 44", "ATTRIBUTE_UOM 44",
    "ATTRIBUTE_LABEL 45", "ATTRIBUTE_VALUE 45", "ATTRIBUTE_UOM 45",
    "ATTRIBUTE_LABEL 46", "ATTRIBUTE_VALUE 46", "ATTRIBUTE_UOM 46",
    "ATTRIBUTE_LABEL 47", "ATTRIBUTE_VALUE 47", "ATTRIBUTE_UOM 47",
    "ATTRIBUTE_LABEL 48", "ATTRIBUTE_VALUE 48", "ATTRIBUTE_UOM 48",
    "ATTRIBUTE_LABEL 49", "ATTRIBUTE_VALUE 49", "ATTRIBUTE_UOM 49",
    "ATTRIBUTE_LABEL 50", "ATTRIBUTE_VALUE 50", "ATTRIBUTE_UOM 50",
    "UPC", "EAN", "GTIN", "UNSPSC", "Warranty", "List Price", "Selling Qty",
    "Selling UOM", "Standard Packaging Information", "LENGTH", "LENGTH_UOM",
    "HEIGHT", "HEIGHT_UOM", "WIDTH", "WIDTH_UOM", "WEIGHT", "WEIGHT_UOM",
    "VOLUME", "VOLUME_UOM", "Product Image", "Alternate Image 1",
    "Alternate Image 2", "Alternate Image 3", "Alternate Image 4", "SDS", "SDS_1",
    "Warranty Information", "Catalog", "Specification Sheet",
    "Instruction/Installation Manual", "Service Manual", "Owners/User Manual",
    "Line Drawing", "MTR", "RoHS", "Full Engineering Drawing",
    "Energy Star Guide", "Technical Bulletin", "Submittal", "Compatibility Chart",
    "Size Chart", "Product Label/Insert", "Video Link", "Video Link 1",
    "Country Of Origin", "Discontinued", "Actual Image (Yes/No)",
]

assert len(DELIVERY_FORMAT_HEADERS) == 252, "DELIVERY_FORMAT_HEADERS must contain exactly 252 items."

# Stage 1: Brand placeholder strings
PLACEHOLDER_STRINGS = {
    "-- unbranded --",
    "-- no unilog brand --",
    "-- no dib brand --",
    "unbranded",
    "no brand",
    "-",
    "none",
    "n/a",
    "null",
    "unknown",
    "undefined",
    ""
}

# Stage 3: Distributor/Cooperative indicators for OEM resolution fallback
DISTRIBUTOR_COOP_PATTERNS = [
    "cooperative", "dealers", "distributor", "distributors", "supply", "wholesale", "adc", "appde"
]

# Known MPN / Product line OEM mapping rules
OEM_MPN_KNOWLEDGE = {
    "PDSH": ("Rheem Manufacturing", "FRIGIDAIRE®", "Professional Series"),
    "WDTS": ("Whirlpool Corporation", "Whirlpool®", "Eco Series"),
}

# Stage 4: Category Keyword Taxonomy Map
TAXONOMY_RULES = [
    {
        "keywords": ["dishwasher", "dish washer", "dishwash"],
        "dept": "Appliances",
        "class": "Large Appliances",
        "fine": "Dishwashers",
        "classpath": "Appliances & Consumer Electronics>Kitchen Appliances>Built-In Dishwashers"
    },
    {
        "keywords": ["bulb", "lamp", "led", "fixture", "light", "chandelier", "sconce", "lantern", "floodlight", "recessed", "vanity"],
        "dept": "Lighting & Electrical",
        "class": "Lighting",
        "fine": "Lamps & Bulbs",
        "classpath": "Lighting & Electrical>Lighting>Lamps & Fixtures"
    },
    {
        "keywords": ["switch", "receptacle", "outlet", "dimmer", "wallplate", "breaker", "wire", "cable", "conduit", "junction"],
        "dept": "Lighting & Electrical",
        "class": "Electrical Controls",
        "fine": "Wiring Devices & Switches",
        "classpath": "Lighting & Electrical>Electrical Controls>Wiring Devices"
    },
    {
        "keywords": ["saw", "blade", "drill", "router", "sander", "grinder", "bit", "driver", "impact", "power tool"],
        "dept": "Tools & Hardware",
        "class": "Power Tools",
        "fine": "Cutting & Drilling Tools",
        "classpath": "Tools & Hardware>Power Tools>Cutting & Drilling Tools"
    },
    {
        "keywords": ["abrasive", "sandpaper", "sanding", "grinding wheel", "flap disc", "buffing", "polishing"],
        "dept": "Abrasives & Industrial",
        "class": "Abrasive Products",
        "fine": "Sanding & Grinding Discs",
        "classpath": "Abrasives & Industrial>Abrasive Products>Discs & Sheets"
    },
    {
        "keywords": ["decking", "deck", "board", "railing", "post", "lumber", "trim", "fascia", "siding", "timbertech", "trex", "azek"],
        "dept": "Building Materials",
        "class": "Decking & Building Products",
        "fine": "Composite Decking & Trim",
        "classpath": "Building Materials>Decking & Building Products>Composite Decking"
    },
    {
        "keywords": ["screw", "bolt", "nut", "washer", "anchor", "fastener", "nail", "rivet"],
        "dept": "Tools & Hardware",
        "class": "Hardware",
        "fine": "Fasteners",
        "classpath": "Tools & Hardware>Hardware>Fasteners"
    },
    {
        "keywords": ["tape", "adhesive", "glue", "epoxy", "sealant", "caulk"],
        "dept": "Adhesives & Tapes",
        "class": "Tapes & Adhesives",
        "fine": "Industrial Tapes",
        "classpath": "Adhesives & Tapes>Tapes & Adhesives>Industrial Tapes"
    },
    {
        "keywords": ["goggles", "glasses", "respirator", "mask", "glove", "harness", "helmet", "safety"],
        "dept": "Safety & Personal Protection",
        "class": "Personal Protective Equipment",
        "fine": "Eye & Face Protection",
        "classpath": "Safety & Personal Protection>Personal Protective Equipment>Eye Protection"
    }
]

# Stage 7: Standard UOM map
STANDARD_UOM_MAP = {
    "in": "in", "inch": "in", "inches": "in", "in.": "in", '"': "in", "''": "in",
    "ft": "ft", "foot": "ft", "feet": "ft", "ft.": "ft", "'": "ft",
    "v": "V", "volt": "V", "volts": "V", "vac": "V", "vdc": "V",
    "a": "A", "amp": "A", "amps": "A", "amperage": "A",
    "w": "W", "watt": "W", "watts": "W",
    "kw": "kW", "kilowatt": "kW", "kilowatts": "kW",
    "kw-hr": "kW-hr", "kwh": "kW-hr", "kw/h": "kW-hr",
    "dba": "dBA", "db": "dBA", "decibel": "dBA", "decibels": "dBA",
    "lb": "lb", "lbs": "lb", "pound": "lb", "pounds": "lb",
    "oz": "oz", "ounce": "oz", "ounces": "oz",
    "hr": "hr", "hrs": "hr", "hour": "hr", "hours": "hr",
    "gal": "gal", "gallon": "gal", "gallons": "gal",
    "psi": "psi", "psig": "psi",
    "°f": "°F", "deg f": "°F", "fahrenheit": "°F",
    "°c": "°C", "deg c": "°C", "celsius": "°C",
    "mm": "mm", "cm": "cm", "m": "m"
}

# Blocked domains for Online Retrieval
BLOCKED_DOMAINS = [
    "amazon.com", "ebay.com", "homedepot.com", "lowes.com", "walmart.com",
    "wayfair.com", "build.com", "supplyhouse.com", "grainger.com", "mcmaster.com",
    "fastenal.com", "ferguson.com", "zoro.com"
]
