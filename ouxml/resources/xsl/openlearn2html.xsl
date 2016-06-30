<?xml version="1.0" encoding="UTF-8"?>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

    <xsl:template match="/">
        <p><xsl:apply-templates/></p>
    </xsl:template>

    <xsl:template match="Paragraph|Reference">
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
        <div class="box core">
        <h2><xsl:value-of select="Heading"/></h2>
        <xsl:apply-templates select="*[not(self::Heading)]"/>
        </div>
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
            <div>
                <xsl:attribute name="name">reveal</xsl:attribute>
                <xsl:attribute name="id"><xsl:value-of select="position()"/></xsl:attribute>
                <xsl:attribute name="class">reveal</xsl:attribute>
                Show answer
            </div>
            <div>
                <xsl:attribute name="id"><xsl:value-of select="concat('answer', position())"/></xsl:attribute>
                <p><xsl:value-of select="Answer"/></p>
            </div>
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

    <xsl:template match="h1">
        <h1><xsl:apply-templates/></h1>
    </xsl:template>

    <xsl:template match="h2">
        <h2><xsl:apply-templates/></h2>
    </xsl:template>

    <xsl:template match="h3">
        <h3><xsl:apply-templates/></h3>
    </xsl:template>

    <xsl:template match="Session/Section/Title">
        <h3 class="subsection"><xsl:apply-templates/></h3>
    </xsl:template>

    <xsl:template match="Table">
        <h2><xsl:value-of select="TableHead"/></h2>
        <table style="width:100%">
            <xsl:for-each select="tbody/tr">
                <tr>
                    <xsl:for-each select="td">
                        <td>
                            <xsl:if test="@rowspan != ''">
                                <xsl:attribute name="rowspan"><xsl:value-of select="@rowspan"/></xsl:attribute>
                            </xsl:if>
                            <xsl:if test="@colspan != ''">
                                <xsl:attribute name="colspan"><xsl:value-of select="@colspan"/></xsl:attribute>
                            </xsl:if>
                            <xsl:apply-templates/>
                        </td>
                    </xsl:for-each>
                </tr>
            </xsl:for-each>
        </table>
    </xsl:template>


</xsl:stylesheet>