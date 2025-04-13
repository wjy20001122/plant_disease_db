import { Chart } from "@/components/ui/chart"
// 等待DOM加载完成
document.addEventListener("DOMContentLoaded", () => {
  // 初始化工具提示
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
  var tooltipList = tooltipTriggerList.map((tooltipTriggerEl) => new bootstrap.Tooltip(tooltipTriggerEl))

  // 初始化弹出框
  var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
  var popoverList = popoverTriggerList.map((popoverTriggerEl) => new bootstrap.Popover(popoverTriggerEl))

  // 文件上传预览
  const fileInput = document.querySelector(".custom-file-input")
  if (fileInput) {
    fileInput.addEventListener("change", function (e) {
      const fileName = e.target.files[0]?.name || "未选择文件"
      const label = this.nextElementSibling
      label.textContent = fileName

      // 如果是图片，显示预览
      if (this.id === "id_image" && e.target.files[0]) {
        const reader = new FileReader()
        reader.onload = (e) => {
          const preview = document.getElementById("image-preview")
          if (preview) {
            preview.src = e.target.result
            preview.style.display = "block"
          }
        }
        reader.readAsDataURL(e.target.files[0])
      }
    })
  }

  // 自动隐藏提示消息
  const alerts = document.querySelectorAll(".alert:not(.alert-permanent)")
  alerts.forEach((alert) => {
    setTimeout(() => {
      const bsAlert = new bootstrap.Alert(alert)
      bsAlert.close()
    }, 5000)
  })

  // 确认删除对话框
  const deleteButtons = document.querySelectorAll(".delete-confirm")
  deleteButtons.forEach((button) => {
    button.addEventListener("click", (e) => {
      if (!confirm("确定要删除此数据吗？此操作不可撤销！")) {
        e.preventDefault()
      }
    })
  })

  // 数据统计图表
  const statsChart = document.getElementById("statsChart")
  if (statsChart) {
    const ctx = statsChart.getContext("2d")
    const data = JSON.parse(statsChart.getAttribute("data-stats"))

    new Chart(ctx, {
      type: "bar",
      data: {
        labels: ["图片", "表格", "ZIP文件"],
        datasets: [
          {
            label: "数据统计",
            data: [data.images_count, data.tables_count, data.zips_count],
            backgroundColor: ["rgba(76, 175, 80, 0.6)", "rgba(33, 150, 243, 0.6)", "rgba(255, 193, 7, 0.6)"],
            borderColor: ["rgba(76, 175, 80, 1)", "rgba(33, 150, 243, 1)", "rgba(255, 193, 7, 1)"],
            borderWidth: 1,
          },
        ],
      },
      options: {
        responsive: true,
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              precision: 0,
            },
          },
        },
      },
    })
  }

  // 图片查看器
  const galleryImages = document.querySelectorAll(".gallery-image")
  if (galleryImages.length > 0) {
    galleryImages.forEach((image) => {
      image.addEventListener("click", function () {
        const modal = new bootstrap.Modal(document.getElementById("imageModal"))
        const modalImage = document.getElementById("modalImage")
        const modalTitle = document.getElementById("imageModalLabel")

        modalImage.src = this.getAttribute("data-full-src") || this.src
        modalTitle.textContent = this.alt
        modal.show()
      })
    })
  }

  // 搜索表单增强
  const searchForm = document.getElementById("searchForm")
  if (searchForm) {
    const clearButton = document.getElementById("clearSearch")
    if (clearButton) {
      clearButton.addEventListener("click", () => {
        const inputs = searchForm.querySelectorAll("input, select")
        inputs.forEach((input) => {
          input.value = ""
        })
        searchForm.submit()
      })
    }
  }
})

// 图片懒加载
document.addEventListener("DOMContentLoaded", () => {
  const lazyImages = [].slice.call(document.querySelectorAll("img.lazy"))

  if ("IntersectionObserver" in window) {
    const lazyImageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const lazyImage = entry.target
          lazyImage.src = lazyImage.dataset.src
          lazyImage.classList.remove("lazy")
          lazyImageObserver.unobserve(lazyImage)
        }
      })
    })

    lazyImages.forEach((lazyImage) => {
      lazyImageObserver.observe(lazyImage)
    })
  } else {
    // 回退到传统的懒加载方法
    let active = false

    const lazyLoad = () => {
      if (active === false) {
        active = true

        setTimeout(() => {
          let lazyImages = [].slice.call(document.querySelectorAll("img.lazy"))
          lazyImages.forEach((lazyImage) => {
            if (
              lazyImage.getBoundingClientRect().top <= window.innerHeight &&
              lazyImage.getBoundingClientRect().bottom >= 0 &&
              getComputedStyle(lazyImage).display !== "none"
            ) {
              lazyImage.src = lazyImage.dataset.src
              lazyImage.classList.remove("lazy")

              lazyImages = lazyImages.filter((image) => image !== lazyImage)

              if (lazyImages.length === 0) {
                document.removeEventListener("scroll", lazyLoad)
                window.removeEventListener("resize", lazyLoad)
                window.removeEventListener("orientationchange", lazyLoad)
              }
            }
          })

          active = false
        }, 200)
      }
    }

    document.addEventListener("scroll", lazyLoad)
    window.addEventListener("resize", lazyLoad)
    window.addEventListener("orientationchange", lazyLoad)
    lazyLoad()
  }
})

