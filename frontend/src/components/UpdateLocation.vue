<template>
    <div>
      <h1>Atualizar Localização</h1>
      <form class="form_latitude" @submit.prevent="updateLocation">
        <label for="latitude">Latitude:</label>
        <input class="input_latitude" type="number" step="any" id="latitude" name="latitude" required>
        <label for="longitude">Longitude:</label>
        <input type="number" class="input_latitude" step="any" id="longitude" name="longitude" required>
        <button type="submit">Atualizar</button>
      </form>
      <button type="button" @click="goToDashboard">Voltar ao Dashboard</button>
    </div>
</template>
  
<script>
  export default {
    name: 'UpdateLocation',
    methods: {
      updateLocation() {
        const latitude = document.getElementById('latitude').value;
        const longitude = document.getElementById('longitude').value;
        try {
          fetch(`http://localhost:8000/api/api/survivors/${this.$route.params.name}/update_location/`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              last_location: `${latitude},${longitude}`
            }),
          });
          alert('Localização atualizada com sucesso!');
          this.$router.push(`/dashboard/${this.$route.params.name}`);
        } catch (error) {
          console.error('Erro ao atualizar localização:', error);
        }
      },
      goToDashboard() {
        this.$router.push(`/dashboard/${this.$route.params.name}`);
      }
    }
  };
</script>

<style>
  .form_latitude {
    display: grid;
    gap: 10px;
    margin-top: 20px;
    justify-items: center;
  }

  label {
    font-size: 1.2rem;
  }

  .input_latitude {
    font-size: 1rem;
    padding: 5px;
    border-radius: 0.375rem;
    border: 1px solid #ccc;
    width: 50%;
  }

  button {
    padding: 10px 20px;
    background-color: #2e8b57;
    color: white;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    font-size: medium;
    margin: 10px
  }

  button:hover {
    background-color: #3cb371;
  }
</style>