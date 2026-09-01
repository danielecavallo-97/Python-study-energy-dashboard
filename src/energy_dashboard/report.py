import matplotlib.pyplot as plt
from pathlib import Path
import analysis

def grafico_mix(mix, paese: str, out_dir="data/output") -> Path:
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6, 6))
    mix.plot.pie(ax=ax, autopct="%1.1f%%")
    ax.set_ylabel("")
    ax.set_title(f"Mix energetico — {paese}")
    path = Path(out_dir) / f"mix_{paese}.png"
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path

def genera_report_html(paese: str, mix_img: Path, out_dir="data/output") -> Path:
    html = f"""
    <html><head><title>Report {paese}</title></head>
    <body>
      <h1>Report energetico — {paese}</h1>
      <img src="{mix_img.name}" width="500">
    </body></html>
    """
    path = Path(out_dir) / f"report_{paese}.html"
    path.write_text(html, encoding="utf-8")
    return path


genera_report_html("IT", grafico_mix(analysis.mix_IT, "IT"))