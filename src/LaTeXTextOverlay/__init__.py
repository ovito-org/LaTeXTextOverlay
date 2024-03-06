#### LaTeX Text Overlay ####
# Render LaTeX text in the viewport

import ovito
from matplotlib.rcsetup import _validators
from ovito.data import DataCollection
from ovito.traits import Color
from ovito.vis import ViewportOverlayInterface
from traits.api import Bool, Code, Enum, Range


class LaTeXTextOverlay(ViewportOverlayInterface):
    text = Code(value="\exp^{i \pi} + 1 = 0", label="Text")
    font = Enum(_validators["mathtext.fontset"].valid.values(), label="Font")
    fontsize = Range(low=1, high=None, value=50, label="Font size")
    if ovito.version >= (3, 10, 3):
        text_color = Color(default=(0.0, 0.0, 0.0), label="Text color")
    else:
        text_color = (0.0, 0.0, 0.0)
    px = Range(low=0.0, high=1.0, value=0.5, label="X position")
    py = Range(low=0.0, high=1.0, value=0.5, label="Y position")
    if ovito.version >= (3, 10, 3):
        show_background = Bool(False, label="Show background")
        background_color = Color(default=(1.0, 0.5, 0.5), label="Background color")

    def render(
        self, canvas: ViewportOverlayInterface.Canvas, data: DataCollection, **kwargs
    ):
        if ovito.version >= (3, 10, 3) and self.show_background:
            bbox = dict(
                boxstyle="round",
                ec=self.background_color,
                fc=self.background_color,
            )
        else:
            bbox = None

        with canvas.mpl_figure(
            pos=(self.px - 0.5, 0.5 + self.py),
            size=(1.0, 1.0),
            anchor="north west",
            alpha=0,
            tight_layout=True,
        ) as fig:
            ax = fig.subplots()
            if self.text:
                ax.text(
                    0.5,
                    0.5,
                    f"${self.text}$",
                    fontsize=self.fontsize,
                    horizontalalignment="center",
                    verticalalignment="center",
                    color=[*self.text_color, 1.0],
                    math_fontfamily=self.font,
                    bbox=bbox,
                )
            ax.axis("off")
