# Venligst ingen filnavne i INPUT_DIR med mellemrum i filnavn!

# Define the directory for input PDFs and output Markdown files
INPUT_DIR := pdfs
OUTPUT_DIR := outputs


# Find all PDF files in the input directory
PDF_FILES := $(wildcard $(INPUT_DIR)/*.pdf)

# Generate a list of corresponding Markdown files in the output directory
MD_FILES := $(patsubst $(INPUT_DIR)/%.pdf,$(OUTPUT_DIR)/%.md,$(PDF_FILES))

# Generate a list of corresponding Pdf files files in the output directory
RESULT_PDF_FILES := $(patsubst $(INPUT_DIR)/%.pdf,$(OUTPUT_DIR)/%.pdf,$(PDF_FILES))

# Generate a list of corresponding word files in the output directory
WORD_FILES := $(patsubst $(INPUT_DIR)/%.pdf,$(OUTPUT_DIR)/%.docx,$(PDF_FILES))

# Define the markdown target to generate all Markdown files
markdown: $(MD_FILES)
	
# Define the markdown target to generate all Markdown files
result_pdf: $(RESULT_PDF_FILES)

# Define the markdown target to generate all Markdown files
word: $(WORD_FILES)

# Define the default target, so it includes markdown result_pdf and word
all: markdown result_pdf word

# Rule to convert PDF to Markdown using dump_to_md.py
$(OUTPUT_DIR)/%.md: $(INPUT_DIR)/%.pdf
	python dump_tabula.py -p --toc -i "$<" > "$@"

# Rule to convert resulting MD to new pdf file, using pandoc
$(OUTPUT_DIR)/%.pdf: $(OUTPUT_DIR)/%.md
	pandoc -i "$<" -o "$@"

# Rule to convert resulting MD to new word file, using pandoc
$(OUTPUT_DIR)/%.docx: $(OUTPUT_DIR)/%.md
	pandoc -i "$<" -o "$@"

# Clean target to remove all generated Markdown files
clean:
	rm -f $(MD_FILES)
	rm -f $(RESULT_PDF_FILES)
	rm -f $(WORD_FILES)
# rm -Force $(MD_FILES)
# rm -Force $(RESULT_PDF_FILES)
# rm -Force $(WORD_FILES)

dump:
	@echo $(PDF_FILES)
	@echo $(MD_FILES)

_:
	@# echo '$(MD_FILES)'
	@# echo $(RESULT_PDF_FILES)
	@# echo $(WORD_FILES)
	
.PHONY: all markdown clean dump
