// Compile this document into a png with:
// typst compile assets/cookbook.typ assets/cookbook.png

#import "@preview/fletcher:0.5.7": diagram, node, edge, shapes
#set text(font: ("Ubuntu Mono", "DejaVu Sans Mono"))
#set page(width: auto, height: auto, margin: 10pt)

#let diagram-style = (node-fill: blue.lighten(50%), node-corner-radius: 5pt,
  node-stroke: .7pt)

#diagram(
  ..diagram-style,debug:0,
  node(enclose:(<repo>, <repo-notebooks>), name:<eo-ds>, fill:blue.lighten(70%), width:5cm),
  node((2,0), name:<repo>, text(weight: "bold")[TUW-Geo\ eo-datascience], stroke:none, fill:none),
  node((2,0.6), name:<repo-chapters>, "chapters/*.qmd", width:3cm),
  node((2,2), name:<repo-notebooks>, "notebooks/*.ipynb *.yml", width:3cm),

  node((0,1), name:<ipynb>, "New content\n*.ipynb *.yml"),
  edge(<ipynb>, (1,1), "b", <repo-notebooks>, "-|>"),
  edge((1,1), "r", <repo-chapters>, "-|>", label:"pre-commit", label-pos:35%, label-side:right),
  node(enclose:((4,0),(4,1)), name:<cook>, fill:blue.lighten(70%), text(weight:"bold")[Pythia\ eo-datascience\
  cookbook]),
  edge(<repo-notebooks>, "r", <cook>, "-|>", label:"release", label-pos:70%, label-side:center),

  node((2,-1), name:<gh-page>, "Internal GH-Pages", shape:shapes.hexagon, fill:blue.lighten(30%)),
  node((4,-1), name:<pythia-page>, "Pythia Gallery", shape:shapes.hexagon, fill:blue.lighten(30%)),
  edge(<eo-ds>, <gh-page>, "-|>", decorations:"wave"),
  edge(<cook>, <pythia-page>, "-|>", decorations:"wave"),
)
