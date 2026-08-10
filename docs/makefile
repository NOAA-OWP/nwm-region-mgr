# Define variables for Sphinx
SPHINXAPIDOC = sphinx-apidoc
SPHINXBUILD = sphinx-build
SOURCEDIR = source
BUILDDIR = build

clean:
	rm -rf $(BUILDDIR)/*
	rm -rf $(SOURCEDIR)/API/_autosummary

html: clean
	$(SPHINXBUILD) -b html $(SOURCEDIR) $(BUILDDIR)
