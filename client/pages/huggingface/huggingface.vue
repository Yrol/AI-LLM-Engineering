<template>
  <div class="w-full max-w-2xl mx-auto">

    <section class="mt-8">
      <h3 class="text-lg font-bold mb-4 border-b pb-2 text-gray-900">Huggingface</h3>

      <!-- Current capabilities -->
      <div class="bg-white shadow-md rounded-lg p-6">
        <h4 class="text-xl font-bold mb-4 border-b border-gray-300 pb-2 text-gray-900">
          Pipelines
        </h4>
        <p>
            The HuggingFace transformers library provides APIs at two different levels.

            The High Level API for using open-source models for typical inference tasks is called "pipelines". It's incredibly easy to use.

            You create a pipeline using something like:

            my_pipeline = pipeline("the_task_I_want_to_do")

            Followed by

            result = my_pipeline(my_input)

            And that's it!

            See end of this colab for a list of all pipelines.
        </p>
      </div>
    </section>
  </div>
</template>


<script setup>
// You can import components or composables here if needed
</script>