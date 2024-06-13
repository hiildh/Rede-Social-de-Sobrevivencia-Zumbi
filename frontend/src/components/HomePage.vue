<template>
  <div class="home">
    <div class="overlay">
      <h1>Junte-se à Rede Social de Sobrevivência Zumbi (ZSSN)</h1>
      <p>Compartilhe Recursos e Informações com Outros Sobreviventes em Tempos de Apocalipse.</p>
      <router-link to="/login" class="btn">Conecte-se com Outros Sobreviventes</router-link>
      <router-link to="/register" class="btn">Cadastre-se como Sobrevivente</router-link>
    </div>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
}
</script>

<style>
  .home {
    text-align: center;
    margin-top: 50px;
    /* background: url('https://images.vexels.com/media/users/3/152583/isolated/preview/761014b6097c79e634089fa680066d0c-pessoas-sentando-ligado-banco-silueta.png?w=360') no-repeat center center; */
    background-size: cover;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #fff;
    position: relative;
    overflow: hidden;
    height: 100%;
  }

  .overlay {
    background-color: rgba(0, 0, 0, 0.5); /* Fundo escuro semitransparente */
    padding: 30px;
    border-radius: 10px;
  }

  h1 {
    font-size: 2.5em;
    margin-bottom: 20px;
  }

  p {
    font-size: 1.2em;
    margin-bottom: 30px;
  }

  .btn {
    display: inline-block;
    padding: 15px 30px;
    background-color: #2e8b57; /* Verde */
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
    margin: 10px;
    transition: background-color 0.3s ease;
  }

  .btn:hover {
    background-color: #3cb371; /* Verde claro */
  }
</style>

