document.getElementById("formRelatorio").addEventListener("submit", async e => {
  e.preventDefault();

  const form = e.target;
  const params = new URLSearchParams(new FormData(form));

  const resp = await fetch(`/api/relatorios?${params}`);

  if (!resp.ok) {
    document.getElementById("resultadoRelatorio").innerHTML = `
      <div class="alert alert-danger">
        Erro ao gerar relatório
      </div>`;
    return;
  }

  const data = await resp.json();

  let html = `
    <div class="card shadow-sm p-3">
      <h6 class="fw-bold">Relatório do período</h6>
      <p>${data.periodo}</p>
  `;

  if (!data.linhas || data.linhas.length === 0) {
    html += `
      <div class="alert alert-warning mt-3">
        Nenhum registro de absenteísmo encontrado para os filtros selecionados.
      </div>
    `;
  } else {
    html += `
      <h6 class="fw-bold text-danger mt-3">
        Top 10 Linhas com Absenteísmo
      </h6>
      <ul class="list-group">
    `;

    data.linhas.forEach(l => {
      html += `
        <li class="list-group-item d-flex justify-content-between">
          ${l.linha}
          <span class="badge bg-danger">${l.total_faltas}</span>
        </li>`;
    });

    html += `</ul>`;
  }

  if (data.cargo_critico) {
    html += `
      <p class="mt-3">
        Observa-se que o cargo
        <strong>${data.cargo_critico.nome}</strong>
        é o que mais registra absenteísmo neste período.
      </p>
    `;
  }

  html += `</div>`;

  document.getElementById("resultadoRelatorio").innerHTML = html;
});
