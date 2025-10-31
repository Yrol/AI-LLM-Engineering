<template>
  <div class="json-viewer">
    <template v-if="parsedData === null && hasInput">
      <div class="error">Invalid JSON format.</div>
    </template>

    <template v-else-if="!hasInput">
      <div class="empty">No data to display.</div>
    </template>

    <template v-else>
      <div v-if="isArray(parsedData)">
        <div v-for="(item, i) in parsedData" :key="i" class="json-item">
          <details open>
            <summary>Index {{ i }}</summary>
            <JsonViewer :data="item" />
          </details>
        </div>
      </div>

      <div v-else-if="isObject(parsedData)">
        <table class="json-table">
          <tbody>
            <tr v-for="(value, key) in parsedData" :key="key">
              <td class="json-key">{{ key }}</td>
              <td class="json-value">
                <template v-if="isPrimitive(value)">
                  {{ formatValue(value) }}
                </template>
                <template v-else>
                  <details open>
                    <summary>Object / Array</summary>
                    <JsonViewer :data="value" />
                  </details>
                </template>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else class="primitive">{{ formatValue(parsedData) }}</div>
    </template>
  </div>
</template>

<script setup>
import { computed } from "vue";

defineProps({
  data: {
    type: [Object, Array, String, Number, Boolean, null],
    required: true,
  },
});

function isArray(v) {
  return Array.isArray(v);
}
function isObject(v) {
  return typeof v === "object" && v !== null && !Array.isArray(v);
}
function isPrimitive(v) {
  return v === null || ["string", "number", "boolean"].includes(typeof v);
}
function formatValue(v) {
  if (typeof v === "string") return `"${v}"`;
  if (v === null) return "null";
  return v;
}

// track whether user passed any input
const hasInput = computed(() => {
  const d = __props.data;
  if (d === null || d === undefined) return false;
  if (typeof d === "string" && d.trim() === "") return false;
  return true;
});

const parsedData = computed(() => {
  const input = __props.data;

  if (!hasInput.value) return []; // empty data, return safe empty

  if (isArray(input) || isObject(input)) return input;

  if (typeof input === "string") {
    try {
      let fixed = input
        .replace(/'/g, '"')
        .replace(/np\.float32\(([\d.eE+-]+)\)/g, "$1")
        .replace(/None/g, "null")
        .replace(/True/g, "true")
        .replace(/False/g, "false");
      return JSON.parse(fixed);
    } catch {
      return null; // signal invalid JSON
    }
  }

  return input;
});
</script>

<style scoped>
.json-viewer {
  font-family: "Fira Code", monospace;
  font-size: 13px;
  background: #fafafa;
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 8px;
  overflow-x: auto;
}

.json-table {
  border-collapse: collapse;
  width: 100%;
}

.json-key {
  font-weight: 600;
  color: #444;
  vertical-align: top;
  padding: 4px 6px;
  width: 150px;
  white-space: nowrap;
}

.json-value {
  padding: 4px 6px;
  color: #111;
}

details {
  border-left: 2px solid #ccc;
  margin: 4px 0 4px 8px;
  padding-left: 8px;
}

summary {
  cursor: pointer;
  font-weight: 500;
  color: #333;
}

.error {
  color: #b00020;
  font-family: monospace;
  font-weight: 600;
}

.empty {
  color: #666;
  font-family: monospace;
  padding: 4px;
  font-style: italic;
}
</style>