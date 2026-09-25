from pathlib import Path
import argparse
import fitz


def render_pdf(pdf_path: Path, dpi: int = 220, force: bool = False, start_page=None, end_page=None) -> None:
    pdf_path = pdf_path.resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"Could not find: {pdf_path}")

    output_dir = pdf_path.parent / f"{pdf_path.stem}_pages"
    output_dir.mkdir(exist_ok=True)

    document = fitz.open(pdf_path)

    total_pages = len(document)
    first = 1 if start_page is None else max(1, start_page)
    last = total_pages if end_page is None else min(total_pages, end_page)

    if first > last:
        raise ValueError("start-page cannot be after end-page")

    zoom = dpi / 72
    matrix = fitz.Matrix(zoom, zoom)

    print(f"PDF: {pdf_path.name}")
    print(f"Total pages: {total_pages}")
    print(f"Rendering pages: {first}-{last}")
    print(f"Output: {output_dir}")
    print(f"DPI: {dpi}")
    print()

    for page_number in range(first, last + 1):
        output_file = output_dir / f"page-{page_number:03d}.png"

        if output_file.exists() and not force:
            print(f"Skipping existing: {output_file.name}")
            continue

        page = document[page_number - 1]

        pixmap = page.get_pixmap(
            matrix=matrix,
            alpha=False,
        )

        pixmap.save(output_file)
        print(f"Rendered: {output_file.name}")

    document.close()
    print("\nDone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Render PDF pages to high-resolution PNG files."
    )

    parser.add_argument("pdf", type=Path, help="Path to PDF file")
    parser.add_argument("--dpi", type=int, default=220, help="Rendering DPI. Default: 220")
    parser.add_argument("--force", action="store_true", help="Overwrite existing rendered pages")
    parser.add_argument("--start-page", type=int, default=None)
    parser.add_argument("--end-page", type=int, default=None)

    args = parser.parse_args()

    render_pdf(
        args.pdf,
        dpi=args.dpi,
        force=args.force,
        start_page=args.start_page,
        end_page=args.end_page,
    )
