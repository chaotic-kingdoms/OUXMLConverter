<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <xsl:apply-templates/>
        </html>
    </xsl:template>


    <xsl:template match="Paragraph">
        &lt;p&gt;<xsl:value-of select="."/>&lt;/p&gt;
    </xsl:template>

    <xsl:template match="BulletedList">
        &lt;ul&gt;
            <xsl:for-each select="ListItem">
                &lt;li&gt;<xsl:value-of select="."/>&lt;/li&gt;
            </xsl:for-each>
        &lt;/ul&gt;
    </xsl:template>

    <xsl:template match="NumberedList">
        <ol>
            <xsl:attribute name="type">
                <xsl:choose>
                    <xsl:when test="@class = 'upper-alpha'">A</xsl:when>
                    <xsl:when test="@class = 'lower-alpha'">a</xsl:when>
                    <xsl:otherwise>1</xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:for-each select="ListItem">
                &lt;li&gt;<xsl:value-of select="."/>&lt;/li&gt;
            </xsl:for-each>
        </ol>
    </xsl:template>


    <xsl:template match="Image">
        <img>
            <xsl:attribute name="src">
                <xsl:value-of select="."/>
            </xsl:attribute>
            <xsl:attribute name="width">100%</xsl:attribute>
        </img>
    </xsl:template>

    <xsl:template match="Caption">
        &lt;p&gt; class="caption">
        <xsl:value-of select="."/>
        &lt;/p&gt;
    </xsl:template>

    <xsl:template match="br">
        &lt;br&gt;
    </xsl:template>

    <xsl:template match="b">
        &lt;b&gt;<xsl:value-of select="."/>&lt;/b&gt;
    </xsl:template>

    <xsl:template match="i">
        &lt;i&gt;<xsl:value-of select="."/>&lt;/i&gt;
    </xsl:template>

</xsl:stylesheet>