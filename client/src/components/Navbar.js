function Navbar() {
  return (
    <nav class="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark" style={{ paddingLeft: "15px" }}>
      <div class="container-fluid">
        <a class="navbar-brand" href="/" style={{ fontWeight: "bold" }}>OLCSript</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
          <div class="navbar-nav">
            <a class="nav-link" href="/errors" target="_blank">Errores</a>
            <a class="nav-link" href="/symbol-table" target="_blank">Tabla de símbolos</a>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
