const abas = document.querySelectorAll(".aba");
abas.forEach(aba => {
  aba.addEventListener("click", () => {
    abas.forEach(a => a.classList.remove("ativa"));
    document.querySelectorAll(".modulo").forEach(m => m.classList.remove("ativo"));
    aba.classList.add("ativa");
    document.getElementById(aba.dataset.alvo).classList.add("ativo");
  });
});

function coletarDados(form) {
  const dados = {};
  form.querySelectorAll("input, select").forEach(el => {
    if (!el.id) return;
    dados[el.id] = el.type === "checkbox" ? el.checked : el.value;
  });
  return dados;
}

document.querySelectorAll(".btn-executar").forEach(btn => {
  btn.addEventListener("click", async () => {
    const modulo = btn.dataset.modulo;
    const form = btn.closest(".modulo").querySelector("form");
    const log = document.getElementById("log-" + modulo);
    const dados = coletarDados(form);

    log.textContent = "Executando, aguarde...\n";

    try {
      const resposta = await fetch("/executar/" + modulo, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(dados),
      });
      const resultado = await resposta.json();
      log.textContent = resultado.log + (resultado.resumo ? "\n\n" + resultado.resumo : "");
    } catch (erro) {
      log.textContent = "Nao foi possivel falar com o servidor. Verifique se 'python servidor.py' esta rodando.";
    }
  });
});