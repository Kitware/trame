<script setup>
import repos from '/repos.json'
import { ref, computed } from 'vue'

const activeTopics = ref(new Set())
const search = ref('')
const sortKey = ref('stars')
const sortDir = ref('desc')

const displayableTopics = {
  "trame-maintenance-program": "Maintenance program",
  "vue2": "Vue2",
  "vue3": "Vue3",
  "...": "Community",
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
    // Hide repos with no displayable topics
    if (!r.topics.includes('trame-component')) {
      return false
    }

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
    if (ka < kb) return -dir
    if (ka > kb) return dir
    return 0
  })
})

const displayableRepoCount = computed(() =>
  repos.filter(r => r.topics.includes('trame-component')).length
)

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

</div>
<div class="tag-filters">
  <div class="tag-filters__buttons">
    <button
      :class="['pill', 'topic', noTopicSelected && 'active']"
      @click="clearFilters()"
    >
      All
    </button>
    <button
      v-for="(label, key) in displayableTopics"
      :key="key"
      :class="['pill', 'topic', activeTopics.has(key) && 'active']"
      @click="toggleTopic(key)"
    >
      {{ label }}
    </button>
  </div>
  <span class="count">
    {{ filtered.length }} / {{ displayableRepoCount }} repos
  </span>
</div>

<table>
  <thead>
    <tr><th>Name</th><th>Description</th><th>Topics</th></tr>
  </thead>
  <tbody>
    <tr v-if="filtered.length === 0">
      <td colspan="3">No repos match your filters.</td>
    </tr>
    <tr v-for="r in filtered" :key="r.name">
      <td>
        <a :href="r.url" target="_blank">
          <img class="repo-img" :src="r.image"/>
        </a>
      </td>
      <td>
        <h4 class="repo-title">
          <span v-if="!r.trustedOwner" title="Non Kitware-owned">⚠️</span>
          <span v-if="r.createdWithinLastYear" title="Created within the last year">🆕</span>
          {{ r.name }}
        </h4>
        {{ r.description || '—' }}
      </td>
      <td>
        <div v-for="t in r.topics" :key="t">
          <a :href="'https://github.com/topics/' + t"
            v-if="displayableTopics[t]"
          >
            <span
              :class="['pill','topic', activeTopics.has(t) && 'active']"
            >
              {{ displayableTopics[t] }}
            </span>
          </a>
        </div>
      </td>
    </tr>
  </tbody>
</table>


<style scoped>
.repo-img {
  max-width: 200px;
}

.pill {
  display: inline-block;
  padding: 2px 7px;
  margin: 2px 2px 2px 0;
  border-radius: 13px;
  border: 1px solid var(--vp-c-divider);
  color: var(--vp-c-text-2);
  background: var(--vp-c-bg);
  cursor: pointer;
}

.repo-title {
  margin: 0px;
}

.tag-filters {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 10px;
  align-items: start;
}

.tag-filters__buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 5px;
}

.count {
  white-space: nowrap;
  padding-top: 2px;
}

.topic {
  margin-bottom: 0;
  line-height: 1;
}

.topic.active {
  font-weight: bold;
}

.topic:hover {
  color: var(--vp-c-brand-1);
}
</style>