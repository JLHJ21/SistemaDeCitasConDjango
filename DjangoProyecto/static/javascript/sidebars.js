let url = window.location.href;

/// Elementos de li
const tabs = ["inicio", "citas", "pacientes", "representantes", "configuracion", "cfg_ct", "citas_admin", "consultorio"];

tabs.forEach(e => {
    /// Agregar .php y ver si lo contiene en la url
    if (url.indexOf(e + ".php") !== -1) {
        /// Agregar tab- para hacer que coincida la Id
        setActive("tab-" + e);
    }

});

/// Funcion que asigna la clase active
function setActive(id) {
    document.getElementById(id).setAttribute("class", "nav-link text-white active");
}