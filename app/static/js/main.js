let inicio = null;

document.getElementById("startTimer").onclick = () => {
  inicio = performance.now();
};

document.getElementById("stopTimer").onclick = () => {
  if (!inicio) return;

  const fim = performance.now();
  const segundos = ((fim - inicio) / 1000).toFixed(2);
  document.getElementById("tempoMontagem").value = segundos;
  inicio = null;
};

document.getElementById("smtForm").addEventListener("submit", async e => {
  e.preventDefault();

  const tempo = document.getElementById("tempoMontagem").value;
  const blank = document.getElementById("blankSMT").value;

  const fd = new FormData();
  fd.append("tempo_montagem", tempo);
  fd.append("blank", blank);

  const r = await fetch("/api/smt/calcular_meta", { method:"POST", body: fd });
  const data = await r.json();

  document.getElementById("resultadoSMT").innerHTML =
    `Meta Hora SMT: <strong>${data.meta_hora}</strong>`;
});

document.getElementById("smtInversoForm").addEventListener("submit", async e => {
  e.preventDefault();

  const fd = new FormData();
  fd.append("meta_hora", document.getElementById("metaHoraInv").value);
  fd.append("blank", document.getElementById("blankInv").value);

  const r = await fetch("/api/smt/calcular_tempo", { method:"POST", body: fd });
  const data = await r.json();

  document.getElementById("resultadoInverso").innerHTML =
    `Tempo de montagem considerado: <strong>${data.tempo_montagem}s</strong>`;
});

async function calcularPCP() {
  const turnos = [];
  document.querySelectorAll('input[type=checkbox]:checked').forEach(c => {
    turnos.push(parseInt(c.value));
  });

  const payload = {
    total_op: document.getElementById("totalOp").value,
    produzido: document.getElementById("produzido").value,
    hora_inicio: document.getElementById("horaInicio").value,
    meta_hora: document.getElementById("metaHora").value,
    blank: document.getElementById("blank").value,
    turnos: turnos,
    refeicao: document.getElementById("refeicao").value === "true"
  };

  const r = await fetch("/api/pcp/calcular", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await r.json();

  let html = "";

  if (data.conclusao) {
    html += `<h5 class="text-success">Conclusão prevista: ${data.conclusao}</h5>`;
  }

  if (data.timeline) {
    html += "<ul>";
    data.timeline.forEach(t => {
      html += `<li>${t.referencia} (${t.inicio} - ${t.fim}): ${t.produzido} placas</li>`;
    });
    html += "</ul>";
  }

  document.getElementById("resultadoPCP").innerHTML = html;
}

