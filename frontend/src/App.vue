<script setup>
import { ref, onMounted } from 'vue';
const leaderboard = ref(null);
const achievements = ref(null);
onMounted(async () => {
  const achievementsResponse = await fetch('http://localhost:8000/achievements');
  achievements.value = await achievementsResponse.json();
  const leaderBoardResponse = await fetch('http://localhost:8000/leaderboard');
  leaderboard.value = await leaderBoardResponse.json();
  leaderboard.value.forEach(leader => {
    leader.bounty = leader.achievement_links.reduce((total, link) => total += link.achievement.bounty, 0);
  });
  leaderboard.value.sort((a, b) => b.bounty - a.bounty);
});
function achievementUnlocked(leader, achievement) {
  const a = leader.achievement_links.find(link => link.achievement_id === achievement.id);
  if (a) {
    return '✅&nbsp;(' + new Date(a.created_at).toLocaleDateString() + ')';
  }    
  return '❌';
}
</script>

<template>
  <div class="container text-center">
    <div class="row">
      <div v-for="leader in leaderboard" :key="leader.id" class="col-4 text-center">
        <div class="card">
          <h1 class="card-title" id="wanted">WANTED</h1>
          <img :src="leader.discord_avatar_url" class="img-top"/>
          <h2 class="card-title" id="dead-or-alive">DEAD OR ALIVE</h2>
          <h2 class="card-title" id="nickname">{{ leader.nick || leader.name }}</h2>
          <div class="card-body">
            <p class="card-text" id="bounty">Bounty: {{ leader.bounty?.toLocaleString() }}</p>
            <table class="table">
              <thead>
                <tr>
                  <th>Achievement</th>
                  <th>Bounty</th>
                  <th>Unlocked</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="achievement in achievements" :key="achievement.id">
                  <td>{{ achievement.name }}</td>
                  <td>{{ achievement.bounty?.toLocaleString() }}</td>
                  <td v-html="achievementUnlocked(leader, achievement)"></td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
    <br />
    <div class="row">
      <table class="table table-striped table-bordered">
        <thead>
          <tr>
            <th>Achievement</th>
            <th>Description</th>
            <th>Bounty</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="achievement in achievements" :key="achievement.id">
            <td>{{ achievement.name }}</td>
            <td>{{ achievement.description }}</td>
            <td>{{ achievement.bounty?.toLocaleString() }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  
</template>

<style scoped>
@font-face {
    font-family: "Century Old Style W02 Bold";
    src: url("https://db.onlinewebfonts.com/t/99183a89d4fca1362ded8ee46f40ed47.eot");
    src: url("https://db.onlinewebfonts.com/t/99183a89d4fca1362ded8ee46f40ed47.eot?#iefix")format("embedded-opentype"),
    url("https://db.onlinewebfonts.com/t/99183a89d4fca1362ded8ee46f40ed47.woff2")format("woff2"),
    url("https://db.onlinewebfonts.com/t/99183a89d4fca1362ded8ee46f40ed47.woff")format("woff"),
    url("https://db.onlinewebfonts.com/t/99183a89d4fca1362ded8ee46f40ed47.ttf")format("truetype"),
    url("https://db.onlinewebfonts.com/t/99183a89d4fca1362ded8ee46f40ed47.svg#Century Old Style W02 Bold")format("svg");
}

#wanted {
  font-family:'Times New Roman', Times, serif;
  font-weight: bold;
}
#dead-or-alive {
  font-family:'Century Old Style W02 Bold', 'Times New Roman', Times, serif;
  font-weight: bold;
}
#nickname {
  font-family:'Century Old Style W02 Bold', 'Times New Roman', Times, serif;
  font-weight: bold;
  font-size: 2em;
}

.card {
  background-color: rgb(214, 193, 168);
}
</style>
