
import xml.etree.ElementTree as gfg

def GenerateXML(fileName) :
	
	root = gfg.Element("History")
	
	m1 = gfg.Element("movement")
	root.append (m1)
	
	b1 = gfg.SubElement(m1, "player")
	b1.text = "Gracz 1"
	b2 = gfg.SubElement(m1, "action")
	b2.text = "Dobral plytke"
	
	m2 = gfg.Element("movement")
	root.append (m2)
	
	c1 = gfg.SubElement(m2, "player")
	c1.text = "Gracz 2"
	c2 = gfg.SubElement(m2, "action")
	c2.text = "Polozyl sekwencje"
	
	
	tree = gfg.ElementTree(root)
	gfg.indent(tree, space="\t", level=0)
	with open (fileName, "wb") as files :
		tree.write(files,encoding="utf-8")

# Driver Code
if __name__ == "__main__":
	GenerateXML("Catalog.xml")


