<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
        <body>
            <xsl:for-each select="Item/Unit/Session">
                <p><xsl:value-of select="Paragraph"/></p>
            </xsl:for-each>

            <xsl:for-each select="Item/Unit/Session/BulletedList">
                <ul>
                    <li><xsl:value-of select="ListItem"/></li>
                </ul>
            </xsl:for-each>
        </body>
        </html>
    </xsl:template>
</xsl:stylesheet>