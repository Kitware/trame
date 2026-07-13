<script setup>
import RepoList from '@theme/RepoList.vue'

const topics = {
  "trame-maintenance-program": "Maintenance program",
  "vtk": "VTK",
  "paraview": "Paraview",
  "3d-slicer*": "3D Slicer",
  "...": "Community",
}
</script>

# Application catalog

⚠️: Non Kitware-owned repository
<br/>

<RepoList filter-topic="trame-app" :displayable-topics="topics" />