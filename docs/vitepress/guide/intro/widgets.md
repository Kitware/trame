<script setup>
import repos from '/repos.json'
import { ref, computed } from 'vue'

const activeTopic = ref(null)

const displayableTopics = {
  "trame-maintenance-program": "Maintained",
  "trame-app": "Application",
  "trame-component": "UI Widget",
  "vtk": "VTK",
  "paraview": "Paraview",
  "3d-slicer": "3D Slicer"
}

const filtered = computed(() => {
  return repos.filter(r => 
    !activeTopic.value || r.topics.includes(activeTopic.value)
  )
})

function toggleTopic(t) {
  activeTopic.value = activeTopic.value === t ? null : t
}
</script>

# Known available widgets

<div class="controls">
  <span class="count">{{ filtered.length }} / {{ repos.length }} repos</span>
</div>

<div class="tag-filters">
  <button :class="['topic', !activeTopic && 'active']" @click="activeTopic = null">All</button>
  <button
    v-for="(label, key) in displayableTopics" :key="key"
    :class="['topic', activeTopic === key && 'active']"
    @click="toggleTopic(key)"
  >{{ label }}</button>
</div>

<table class="repo-table">
  <thead>
    <tr><th>Name</th><th>Description</th><th>Topics</th></tr>
  </thead>
  <tbody>
    <tr v-if="filtered.length === 0">
      <td colspan="3" class="empty">No repos match your filters.</td>
    </tr>
    <tr v-for="r in filtered" :key="r.name">
      <td><a :href="r.url" target="_blank">{{ r.name }}</a><img :src="r.image"/></td>
      <td class="desc">{{ r.description || '—' }}</td>
      <td>
        <div v-for="t in r.topics" :key="t">
          <span
            v-if="displayableTopics[t]"
            :class="['topic', activeTopic === t && 'active']"
            @click="toggleTopic(t)"
          >{{ displayableTopics[t] }}</span>
        </div>
      </td>
    </tr>
  </tbody>
</table>

<style scoped>
img {
  max-width: 200px;
} 
.topic {
  display: inline-block; 
  padding: 2px 7px;
  margin: 2px 2px 2px 0;
  border-radius: 20px;
  border: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
  cursor: pointer;
} 
.topic:hover, .topic.active {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
}
</style>