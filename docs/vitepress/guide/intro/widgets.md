<script setup>
import repos from '/repos.json'
import { ref, computed } from 'vue'

const activeTopics = ref(new Set())
const search = ref('')

const displayableTopics = {
  "trame-maintenance-program": "Maintained",
  "trame-app": "Application",
  "trame-component": "UI Widget",
  "vtk": "VTK",
  "paraview": "Paraview",
  "3d-slicer": "3D Slicer"
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return repos.filter(r => {
    const matchesTopics = 
      activeTopics.value.size === 0 ||
      [...activeTopics.value].every(t => r.topics.includes(t))
    const matchesSearch = 
      !q || 
      r.name.toLowerCase().includes(q) ||
      (r.description && r.description.toLowerCase().includes(q)) ||
      r.topics.some(t => t.toLowerCase().includes(q))
    return matchesTopics && matchesSearch
  })
})

const noTopicSelected = computed(() => {
  return activeTopics.value.size === 0
})

const clearFilters = () => {
  activeTopics.value = new Set() 
}

function toggleTopic(t) {
  const s = new Set(activeTopics.value)
  s.has(t) ? s.delete(t) : s.add(t)
  activeTopics.value = s
}
</script>

# Known available widgets

<br/>
<div class="controls">
  <input v-model="search" class="search" placeholder="Search repos…" />
  <span class="count">{{ filtered.length }} / {{ repos.length }} repos</span>
</div>

<div class="tag-filters">
  <button
    :class="['topic', noTopicSelected && 'active']" 
    @click="clearFilters()"
  >
    All
  </button>
  <button
    v-for="(label, key) in displayableTopics" :key="key"
    :class="['topic', activeTopics.has(key) && 'active']"
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
      <td>
        <div v-if="!r.trustedOwner">⚠️</div>
        <a :href="r.url" target="_blank">{{ r.name }}</a>
        <img :src="r.image"/></td>
      <td class="desc">
        {{ r.description || '—' }}
      </td>
      <td>
        <div v-for="t in r.topics" :key="t">
          <span
            v-if="displayableTopics[t]"
            :class="['topic', activeTopics.has(t) && 'active']"
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
.search{
  display: inline-block; 
  padding: 2px 7px;
  margin: 2px 2px 2px 0;
  border-radius: 10px;
  border: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
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