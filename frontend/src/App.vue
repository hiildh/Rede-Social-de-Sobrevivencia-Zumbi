<template>
  <div class="home">
  <h1>Bem-vindo à Rede Social de Sobrevivência Zumbi (ZSSN)</h1>
  <p>Aqui você pode compartilhar recursos e informações com outros sobreviventes.</p>
  <router-link to="/survivors" class="btn">Ver Sobreviventes</router-link>
  </div>
</template>

<script>

export default {
  name: 'App',
}
</script>

<style>
  .home {
    text-align: center;
    margin-top: 50px;
  }
  .btn {
    display: inline-block;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    text-decoration: none;
    border-radius: 5px;
    margin-top: 20px;
  }
  .btn:hover {
    background-color: #0056b3;
  }
</style>
