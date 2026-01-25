document.getElementById("formRelatorio").addEventListener("submit", async e => {
  e.preventDefault();

  const params = new URLSearchParams(new FormData(e.target));
  const resp = await fetch(`/api/relatorios?${params}`);
  const data = await resp.json();

  let html = `
    <div class="card shadow-sm p-4 mb-4">
      <h5 class="fw-bold">Relatório Gerencial</h5>
      <small class="text-muted">${data.periodo}</small>
    </div>

    <div class="row g-3 mb-4 text-center">
      <div class="col-md-4">
        <div class="card p-3 shadow-sm">
          <small>Total de Faltas</small>
          <h3 class="text-danger">${data.kpis.total_faltas}</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 shadow-sm">
          <small>Linhas Afetadas</small>
          <h3>${data.kpis.linhas_afetadas}</h3>
        </div>
      </div>

      <div class="col-md-4">
        <div class="card p-3 shadow-sm">
          <small>Linhas Monitoradas</small>
          <h3>${data.kpis.linhas_totais}</h3>
        </div>
      </div>
    </div>

    <div class="card shadow-sm p-3 mb-4">
      <h6 class="fw-bold text-danger">
        Top Linhas com Maior Impacto
      </h6>
      <ul class="list-group list-group-flush">
        ${data.linhas.map(l => `
          <li class="list-group-item d-flex justify-content-between">
            ${l.linha}
            <span class="badge bg-danger">${l.total_faltas}</span>
          </li>
        `).join("")}
      </ul>
    </div>

    <div class="alert alert-secondary">
      <strong>Insight Automático:</strong>
      ${data.insight}
    </div>
  `;

  document.getElementById("resultadoRelatorio").innerHTML = html;
});
