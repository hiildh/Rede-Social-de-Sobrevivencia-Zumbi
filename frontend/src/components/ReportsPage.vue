<template>
    <div class="reports-page">
        <h1>Relatórios</h1>
        <div v-if="reports" class="reports-container">
            <table>
                <thead>
                    <tr>
                        <th>Métrica</th>
                        <th>Valor</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Porcentagem de sobreviventes infectados</td>
                        <td>{{ reports.infected_percentage.toFixed(2) }}%</td>
                    </tr>
                    <tr>
                        <td>Porcentagem de sobreviventes não infectados</td>
                        <td>{{ reports.uninfected_percentage.toFixed(2) }}%</td>
                    </tr>
                    <tr>
                        <td>Quantidade média de recursos por sobrevivente</td>
                        <td>
                            <ul>
                                <li>Água: {{ reports.avg_water.toFixed(2) }}</li>
                                <li>Alimentação: {{ reports.avg_food.toFixed(2) }}</li>
                                <li>Medicação: {{ reports.avg_medication.toFixed(2) }}</li>
                                <li>Munição: {{ reports.avg_ammunition.toFixed(2) }}</li>
                            </ul>
                        </td>
                    </tr>
                    <tr>
                        <td>Pontos perdidos devido a sobreviventes infectados</td>
                        <td>{{ reports.infected_points_lost }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-else>
            <p>Carregando relatórios...</p>
        </div>
    </div>
</template>

<script>
    export default {
        name: 'ReportsPage',
        data() {
            return {
                reports: null
            };
        },
        async created() {
            try {
                const response = await fetch('http://localhost:8000/api/reports/');
                if (response.ok) {
                    this.reports = await response.json();
                } else {
                    throw new Error('Erro ao buscar relatórios');
                }
            } catch (error) {
                alert('Erro: ' + error.message);
            }
        },
    };
</script>

<style scoped>
.reports-page {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    font-family: Arial, sans-serif;
}

.reports-container {
    background-color: #3cb37257;
    border: 1px solid #016910;
    padding: 15px;
    margin-top: 20px;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin-top: 10px;
}

th, td {
    border: 1px solid #073801;
    padding: 8px;
    text-align: left;
}

th {
    background-color: #1c9e105d;
}

td {
    background-color: #f0f0f0;
}

ul {
    list-style-type: none;
    padding-left: 0;
    margin-top: 5px;
}

ul li {
    margin-bottom: 5px;
}

ul li:last-child {
    margin-bottom: 0;
}
</style>
