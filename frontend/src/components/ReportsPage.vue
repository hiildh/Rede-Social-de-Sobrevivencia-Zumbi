<template>
    <div>
        <h1>Relatórios</h1>
        <!-- Exibir relatórios -->
    </div>
</template>

<script>
    export default {
        name: 'ReportsPage',
        data() {
        return {
            reports: {}
        };
        },
        async created() {
        try {
            const response = await fetch('http://localhost:8000/api/reports');
            if (response.ok) {
            this.reports = await response.json();
            } else {
            throw new Error('Erro ao buscar relatórios');
            }
        } catch (error) {
            alert('Erro: ' + error.message);
        }
        }
    };
</script>
