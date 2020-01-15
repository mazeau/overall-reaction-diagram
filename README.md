# Overall reaction path daigrams

This is for use with Cantera to generate overall reaction path diagrams that follow the mass flux through the entire system, including both gas and surface systems.

To use, run a Cantera simulation (or one of the test simulations).
A dot file titled `integration_flux_data.dot` will be created.
Then, run `dot -Tpdf integration_flux_data.dot -ooverallpathway.pdf` to generate a pdf.
