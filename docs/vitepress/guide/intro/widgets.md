<script setup>
import repos from '/repos.json'
import { ref, computed } from 'vue'

const activeTopics = ref(new Set())
const search = ref('')
const sortKey = ref('stars')
const sortDir = ref('desc')

const displayableTopics = {
  "trame-maintenance-program": "Maintenance program",
  "trame-app": "Application",
  "trame-component": "UI Widget",
  "vtk": "VTK",
  "paraview": "Paraview",
  "3d-slicer": "3D Slicer",
  "vue2": "Vue2",
  "vue3": "Vue3"
}

const sortOptions = {
  name: { label: 'Name (A-Z)', key: r => r.name.toLowerCase() },
  stars: { label: 'Stars', key: r => r.stars },
  lastCommitDate: { label: 'Last contribution', key: r => new Date(r.lastCommitDate).getTime() },
  createdAt: { label: 'Creation date', key: r => new Date(r.createdAt).getTime() },
  commitCount: { label: 'Commits', key: r => r.commitCount },
  pullRequestCount: { label: 'Pull requests', key: r => r.pullRequestCount },
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  const list = repos.filter(r => {
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

  const { key } = sortOptions[sortKey.value]
  const dir = sortDir.value === 'asc' ? 1 : -1
  return [...list].sort((a, b) => {
    const ka = key(a), kb = key(b)
    if (ka < kb) return -1 * dir
    if (ka > kb) return 1 * dir
    return 0
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

function toggleSortDir() {
  sortDir.value = sortDir.value === 'asc' ? 'desc' : 'asc'
}
</script>

# Known available widgets


⚠️: Non Kitware-owned repository
<br/>
<div class="controls">
  <input v-model="search" class="pill" placeholder="Search repos…" />

  <select v-model="sortKey" class="pill">
    <option v-for="(opt, key) in sortOptions" :key="key" :value="key">
      Sort by: {{ opt.label }}
    </option>
  </select>

  <button class="pill" @click="toggleSortDir" :title="sortDir === 'asc' ? 'Ascending' : 'Descending'">
    {{ sortDir === 'asc' ? '↑' : '↓' }}
  </button>

  <span class="count">{{ filtered.length }} / {{ repos.length }} repos</span>
</div>

<div class="tag-filters">
  <button
    :class="['pill', 'topic', noTopicSelected && 'active']" 
    @click="clearFilters()"
  >
    All
  </button>
  <button
    v-for="(label, key) in displayableTopics" :key="key"
    :class="['pill', 'topic', activeTopics.has(key) && 'active']"
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
        <div v-if="!r.trustedOwner" title="Non Kitware-owned">⚠️</div>
        <div v-if="r.createdWithinLastYear" title="Created within the last year">🆕</div>
        <a :href="r.url" target="_blank">{{ r.name }}</a>
        <img :src="r.image"/></td>
      <td class="desc">
        {{ r.description || '—' }}
      </td>
      <td>
        <div v-for="t in r.topics" :key="t">
          <span
            v-if="displayableTopics[t]"
            :class="['pill', 'topic', activeTopics.has(t) && 'active']"
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
.pill {
  display: inline-block;
  padding: 2px 7px;
  margin: 2px 2px 2px 0;
  border-radius: 20px;
  border: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  cursor: pointer;
}
.topic:hover, .topic.active {
  border-color: var(--vp-c-brand-1);
  color: var(--vp-c-brand-1);
  background: var(--vp-c-brand-soft);
}
</style>