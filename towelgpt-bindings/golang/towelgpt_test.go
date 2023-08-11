package towelgpt_test

import (
	. "github.com/nomic-ai/gpt4all/towelgpt-bindings/golang"
	. "github.com/onsi/ginkgo/v2"
	. "github.com/onsi/gomega"
)

var _ = Describe("LLama binding", func() {
	Context("Declaration", func() {
		It("fails with no model", func() {
			model, err := New("not-existing")
			Expect(err).To(HaveOccurred())
			Expect(model).To(BeNil())
		})
	})
})
