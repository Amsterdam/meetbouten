# Meetbouten

Bewaking verzakkingen middels meetpunten op gebouwen en straat-elementen.
De applicatie beheert landmeetkundige grondslag xy, NAP- bouten, referentiebouten en deformatiebouten  in een ruimtelijke database. Grondslagpunten en hoogtebouten kunnen worden toegevoegd, gemuteerd of geraadpleegd. Er wordt ook historie bijgehouden van de hoogtebouten. Foto’s van de grondslagpunten en foto’s en **grafieken van de hoogtebouten** kunnen worden getoond. Tevens is het mogelijk **resultaten van waterpassingen te vergelijken met de grondslagdatabase** en worden er **invoerbestanden voor het vereffeningspakket MOVE3 van de Grontmij aangemaakt.** De resultaten van NAP-metingen en deformatiemetingen (meetboutengis) worden ontsloten via Generieke Ontsluiting Basisgegevens (GOB) bij Datapunt.

### Technische eigenschappen

NAP heeft een Client op ADW waarmee de meetresultaten rechtstreeks in de Oracle Database  (DB) geschreven worden en foto’s op een centrale netwerkschijf  opgeslagen. In de DB staan harde paden naar de foto’s op de centrale netwerkschijf.
GOB raadpleegt de NAP DB. **Functioneel Beheer (FB) werkt rechtstreeks op de DB middels SQL-Developer.** Er is een Test, Acceptatie en een Productie omgeving.
