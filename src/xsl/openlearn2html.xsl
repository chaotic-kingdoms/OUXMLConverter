<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <html>
            <xsl:apply-templates/>
        </html>
    </xsl:template>

    <xsl:template match="Paragraph">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="BulletedList|BulletedSubsidiaryList">
        <ul>
            <xsl:for-each select="ListItem">
                <li><xsl:apply-templates/></li>
            </xsl:for-each>
        </ul>
    </xsl:template>

    <xsl:template match="NumberedList|NumberedSubsidiaryList">
        <ol>
            <xsl:attribute name="type">
                <xsl:choose>
                    <xsl:when test="@class = 'upper-alpha'">A</xsl:when>
                    <xsl:when test="@class = 'lower-alpha'">a</xsl:when>
                    <xsl:otherwise>1</xsl:otherwise>
                </xsl:choose>
            </xsl:attribute>
            <xsl:for-each select="ListItem">
                <li><xsl:apply-templates/></li>
            </xsl:for-each>
        </ol>
    </xsl:template>


    <xsl:template match="Image">
        <img>
            <xsl:attribute name="src"><xsl:value-of select="@src"/></xsl:attribute>
        </img>
    </xsl:template>

    <xsl:template match="Caption">
        <p class="caption">
        <xsl:value-of select="."/>
        </p>
    </xsl:template>

    <xsl:template match="Box">
        <p class="box activity">
        <h2><xsl:value-of select="Heading"/></h2>
        <xsl:apply-templates select="*[not(self::Heading)]"/>
        </p>
    </xsl:template>

    <xsl:template match="CaseStudy">
        <p class="box casestudy">
        <h2><xsl:value-of select="Heading"/></h2>
        <xsl:apply-templates select="*[not(self::Heading)]"/>
        </p>
    </xsl:template>

    <xsl:template match="ITQ">
        <div class="box question">
        <p><xsl:value-of select="Question"/></p>
        <div name="reveal" id="2" class="reveal">Show answer</div>
        <div style="display:none;" id="answer2"><xsl:value-of select="Answer"/></div>
        </div>
    </xsl:template>

    <xsl:template match="br">
        <br />
    </xsl:template>

    <xsl:template match="b">
       <b><xsl:apply-templates/></b>
    </xsl:template>

    <xsl:template match="i">
        <i><xsl:apply-templates/></i>
    </xsl:template>

    <xsl:template match="a">
        <a>
            <xsl:attribute name="href"><xsl:value-of select="@href"/></xsl:attribute>
            <xsl:value-of select="."/>
        </a>
    </xsl:template>


</xsl:stylesheet>