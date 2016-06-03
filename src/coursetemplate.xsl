<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <xsl:apply-templates/>
        </html>
    </xsl:template>

    <xsl:template match="BulletedList">
        &lt;ul&gt;
            <xsl:for-each select="ListItem">
                &lt;li&gt;<xsl:value-of select="."/>&lt;/li&gt;
            </xsl:for-each>
        &lt;/ul&gt;
    </xsl:template>

    <xsl:template match="Paragraph">
        &lt;p&gt;<xsl:value-of select="."/>&lt;/p&gt;
    </xsl:template>

    <xsl:template match="Image">
        <img>
            <xsl:attribute name="src">
                <xsl:value-of select="."/>
            </xsl:attribute>
        </img>
    </xsl:template>

    <xsl:template match="br">
        &lt;br&gt;
    </xsl:template>


</xsl:stylesheet>