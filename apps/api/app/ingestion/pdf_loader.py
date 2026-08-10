import logging
import argparse
from pypdf import PdfReader
from pathlib import Path
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class LoadedDocument:
        source_path: str
        filename: str
        text: str
        num_pages: int


def load_pdf(path: str | Path) -> LoadedDocument:
        '''Open a pdf and extract text page by page.'''
        path = Path(path)
        reader = PdfReader(path)

        pages = [page.extract_text() or "" for page in reader.pages]
        text = "\n".join(pages).strip()

        if not text:
                logger.warning("NO extractable text in %s", path.name)
        
        return LoadedDocument(str(path), path.name, text, len(reader.pages))


def load_folder(directory: str | Path, recursive: bool = True) -> list[LoadedDocument]:
        '''Load all PDF in a folder. Skips files that fail to parse.'''
        directory = Path(directory)
        # ** means “any number of directory levels”
        pattern = "**/*.pdf" if recursive else "*.pdf"

        documents: list[LoadedDocument] = []
        for path in sorted(directory.glob(pattern)):
                try:
                        documents.append(load_pdf(path))
                except Exception as e:
                        logger.error('Failed to load %s: %s', path, e)
                        continue

        logger.info("Loaded %d PDF(s) from %s", len(documents), directory)
        return documents

def main() -> None:
        parser = argparse.ArgumentParser()
        parser.add_argument("directory")
        parser.add_argument("--recrusive", action="store_true")
        args = parser.parse_args()

        docs = load_folder(args.directory, args.recrusive)
        for doc in docs:
                print(f"{doc.filename}: {doc.num_pages} pages, {len(doc.text)} chars")

if __name__ == "__main__":
        main()
