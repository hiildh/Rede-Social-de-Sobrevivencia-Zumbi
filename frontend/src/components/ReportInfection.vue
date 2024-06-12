<template>
  <div>
    <h1>Reportar Infecção</h1>
    <form class="form_infection" @submit.prevent="reportInfection">
      <label for="reported_survivor_name">Nome do infectado:</label>
      <input type="text" class="input_infection" id="reported_survivor_name" v-model="reportedSurvivorName" required>
      <button type="submit">Reportar Infecção</button>
    </form>
    <button type="button" @click="goToDashboard">Voltar ao Dashboard</button>
  </div>
</template>

<script>
  export default {
    name: 'ReportInfection',
    data() {
      return {
        reportedSurvivorName: ''
      };
    },
    methods: {
      async reportInfection() {
        const reporterName = this.$route.params.name;
        const reportedSurvivorName = this.reportedSurvivorName;

        try {
          const response = await fetch(`http://localhost:8000/api/api/survivors/${reportedSurvivorName}/mark_infected/`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              reporter_name: reporterName,
            }),
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Erro ao reportar infecção');
          }

          const data = await response.json();
          alert(data.status);
          this.$router.push(`/dashboard/${reporterName}`);
        } catch (error) {
          console.error('Erro ao reportar infecção:', error);
          alert(error.message);
        }
      },
      goToDashboard() {
        this.$router.push(`/dashboard/${this.$route.params.name}`);
      }
    }
  };
</script>

<style>
  .form_infection {
  display: grid;
  gap: 10px;
  margin-top: 20px;
  justify-items: center;
  }

  label {
  font-size: 1.2rem;
  }

  .input_infection {
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
