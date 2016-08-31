Floats, Figures, and Tables
===============================================================================

<!-- PAGETOC -->

Figures
-------------------------------------------------------------------------------

Ei oratio mediocritatem sea, at choro mandamus disputando quo, id eius
albucius deseruisse mei. Id eam verear disputando repudiandae. Per et
clita reformidans. Ea his corpora ancillae fabellas, an eum facer tation
populo. Vix omittam lucilius inciderint ne, est cu civibus scribentur
adversarium.

![The scale of the universe mapped to the branches of science and the hierarchy of science. CC BY-SA 3.0 (2013)
    [Wikimedia Commons](https://en.wikipedia.org/wiki/Science#/media/File:The_Scientific_Universe.png).
    ](img/1024px-the_scientific_universe.png) {#fig:scientific_universe}

[@Fig:scientific_universe] shows some cool things.

Ei oratio mediocritatem sea, at choro mandamus disputando quo, id eius
albucius deseruisse mei. Id eam verear disputando repudiandae. Per et
clita reformidans. Ea his corpora ancillae fabellas, an eum facer tation
populo. Vix omittam lucilius inciderint ne, est cu civibus scribentur
adversarium.

Pro solet accumsan at. Id has dicunt corrumpit, vel in mundi vitae
definiebas, eos in dicunt aliquando. His falli qualisque eu, ad vim movet
dolor, per ne denique lobortis. Recusabo tractatos per cu. Apeirian
voluptaria constituam eam no. Scripta vivendum mel ne.


Lorem ipsum dolor sit amet, duo ut putant verear, nam ut brute utroque.
Officiis qualisque conceptam te duo, eu vim soluta numquam, has ut aliquip
accusamus. Probo aliquam pri id. Mutat singulis ad vis, eam euismod pertinax
an, ea tale volumus vel. At porro soleat est. Debet facilis admodum an sed,
at falli feugiat est.

Ne nonumy quodsi petentium vix, mel ad errem accusata periculis. Porro
urbanitas consetetur mei eu, his nisl officiis ei. Ei cum fugit graece,
ne qui tantas qualisque voluptaria. Vis ut laoreet euripidis, vix aeque
omittam at, vix no cetero volumus. Per te omnium volutpat torquatos, cu vis
sumo decore. Eirmod hendrerit an pri.

![The observed (solid) local $p_{0}$ as a function of $m_{H}$ in the low mass range.
    The dashed curve shows the expected local $p_{0}$ under the hypothesis of a
    SM Higgs boson signal at that mass with its $\pm{}1\sigma$ band.
    The horizontal dashed lines indicate the $p$-values corresponding to
    significances of 1 to 6$\sigma$&nbsp;[@ATLAS_2012_Observation_of_a_new_particle_in_the_search_for]\.
    ](img/ATLAS-local-p0-vs-mH.png) {#fig:ATLAS_local_p0_vs_mH}

[@Fig:ATLAS_local_p0_vs_mH] shows the $p_{0}$ value as a function of the reconstructed Higgs mass
from the ATLAS experiment.

Amet magna voluptatum eam eu. Denique moderatius ad pri, an vix tale
referrentur, atqui appetere et eos. Pri esse disputationi et. Te his
assum persius, in eam deterruisset consequuntur. Quando signiferumque no
his, usu nusquam corrumpit ex, sea ex soluta option facilisis. Ne autem
assentior consequuntur nam, constituto scripserit no eam. Eu laoreet
fabellas postulant eos.


Tables
-------------------------------------------------------------------------------

Ei oratio mediocritatem sea, at choro mandamus disputando quo, id eius
albucius deseruisse mei. Id eam verear disputando repudiandae. Per et
clita reformidans. Ea his corpora ancillae fabellas, an eum facer tation
populo. Vix omittam lucilius inciderint ne, est cu civibus scribentur
adversarium.


Table: Approximate number of readout channels per sub-detector in ATLAS for the primary sub-detectors (ignoring the minbias trigger system, luminosity monitors, and DCS sensors) [@ATLAS_2008_The_ATLAS_Experiment_at_the_CERN_Large_Hadron]. {#tbl:atlas_channels}

| System                | Subsystem     |  Approx. channels |
|:----------------------|:--------------|------------------:|
| Inner detector        | Pixels        |              80 M |
|                       | SCT           |             6.3 M |
|                       | TRT           |             350 k |
| EM Calorimeter        | LAr barrel    |             110 k |
|                       | LAr end-cap   |              64 k |
| Hadronic Calorimeter  | Tile barrel   |             9.8 k |
|                       | LAr end-cap   |             5.6 k |
|                       | LAr forward   |             3.5 k |
| Muon spectrometer     | MDTs          |             350 k |
|                       | CSCs          |              31 k |
|                       | RPCs          |             370 k |
|                       | TGCs          |             320 k |
| Total                 |               |              88 M |


Pro solet accumsan at. Id has dicunt corrumpit, vel in mundi vitae
definiebas, eos in dicunt aliquando. His falli qualisque eu, ad vim movet
dolor, per ne denique lobortis. Recusabo tractatos per cu. Apeirian
voluptaria constituam eam no. Scripta vivendum mel ne.

[@Tbl:atlas_channels] shows some cool things too.


Table of contents per html page
------------------------------------------------------

To insert a table of contents for a single html page,
add the following line to the Markdown, probably near
the top of the page as is done for this one.

    <!-- PAGETOC -->


Clickmore
-------------------------------------------------------------------------------

You can hide parts of a document in a heading that needs to be clicked
to show more by making a `div` of class `clickmore`
and a `div` of class `more`, linked to eachother like this:

    <div class="clickmore"><a id="link:test1" class="closed" onclick="toggle_more('test1')">Click for more details</a></div>
    <div id="test1" class="more">

    Ne nonumy quodsi petentium vix, mel ad errem accusata periculis. Porro
    urbanitas consetetur mei eu, his nisl officiis ei. Ei cum fugit graece,
    ne qui tantas qualisque voluptaria. Vis ut laoreet euripidis, vix aeque
    omittam at, vix no cetero volumus. Per te omnium volutpat torquatos, cu vis
    sumo decore. Eirmod hendrerit an pri.
    
    ...
    
    </div>

For example:

<div class="clickmore"><a id="link:test1" class="closed" onclick="toggle_more('test1')">Click for more details</a></div>
<div id="test1" class="more">

Ne nonumy quodsi petentium vix, mel ad errem accusata periculis. Porro
urbanitas consetetur mei eu, his nisl officiis ei. Ei cum fugit graece,
ne qui tantas qualisque voluptaria. Vis ut laoreet euripidis, vix aeque
omittam at, vix no cetero volumus. Per te omnium volutpat torquatos, cu vis
sumo decore. Eirmod hendrerit an pri.

Amet magna voluptatum eam eu. Denique moderatius ad pri, an vix tale
referrentur, atqui appetere et eos. Pri esse disputationi et. Te his
assum persius, in eam deterruisset consequuntur. Quando signiferumque no
his, usu nusquam corrumpit ex, sea ex soluta option facilisis. Ne autem
assentior consequuntur nam, constituto scripserit no eam. Eu laoreet
fabellas postulant eos.

Ei oratio mediocritatem sea, at choro mandamus disputando quo, id eius
albucius deseruisse mei. Id eam verear disputando repudiandae. Per et
clita reformidans. Ea his corpora ancillae fabellas, an eum facer tation
populo. Vix omittam lucilius inciderint ne, est cu civibus scribentur
adversarium.

Pro solet accumsan at. Id has dicunt corrumpit, vel in mundi vitae
definiebas, eos in dicunt aliquando. His falli qualisque eu, ad vim movet
dolor, per ne denique lobortis. Recusabo tractatos per cu. Apeirian
voluptaria constituam eam no. Scripta vivendum mel ne.

I wonder if [@Tbl:label] works.

Table: Caption {#tbl:label}

a   b   c
--- --- ---
1   2   3
4   5   6

</div> <!-- end clickmore -->


<!-- REFERENCES -->


