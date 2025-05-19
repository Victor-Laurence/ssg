# Running the script
Using the WSL terminal, within the root directory:
* ./test.sh
or
* ./main.sh
or
* ./build.sh

# How the SSG works
When running the main.sh, it will launch a webserver on localhost:8888
Here's a rough outline of what this static site generator will do when it runs:

1. Delete everything in the /public directory.
2. Copy any static assets (HTML template, images, CSS, etc.) to the /public directory.
3. Generate an HTML file for each Markdown file in the /content directory. For each Markdown file:
 * Open the file and read its contents.
 * Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
 * Convert each block into a tree of HTMLNode objects. For inline elements (like bold text, links, etc.) we will convert:
   - Raw markdown -> TextNode -> HTMLNode
 * Join all the HTMLNode blocks under one large parent HTMLNode for the pages.
 * Use a recursive to_html() method to convert the HTMLNode and all its nested nodes to a giant HTML string and inject it in the HTML template.
 * Write the full HTML string to a file for that page in the /public directory.