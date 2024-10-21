GitHub's README files, written in Markdown, do not natively support LaTeX-style math notation (like `\[ ... \]` or `\frac{...}{...}`). To format equations properly in Markdown, you can either use plain text or integrate LaTeX equations by taking a screenshot of the equations or using a Markdown flavor that supports math, like MathJax (but this is not supported by GitHub). 

For a clean and simple README, here's a modified version where the formulas are represented using plain text:

---

# Human Visual

This README explores key visual concepts, including why objects appear colorless in moonlight, visual adaptation when moving from bright to dark environments, and resolving power of the human eye and cameras.

---

### 1. **Why do objects appear colorless under moonlight?**
- In bright daylight, **cones** in our eyes are active and sensitive to color, which is why objects appear brightly colored.
- Under dim moonlight, the **rods** in our eyes become more active. Rods are more sensitive to low light but do not perceive color.
- As a result, objects seen by moonlight appear as **colorless forms** because our rods dominate vision in low light conditions, while cones become less effective.

---

### 2. **Smallest Discernible Dot Diameter by the Human Eye**
- **Problem:** Estimate the diameter of the smallest dot the eye can discern if the page is 0.2 meters away.
  
  **Given:**
  - Fovea dimensions: 1.5 mm x 1.5 mm
  - Number of cones in the fovea: ~337,000 (arranged in a 580x580 grid)

  **Steps:**
  - The diameter of a single cone can be approximated by dividing the fovea length by the total number of cones and spaces in one row.
  - Number of elements (cones): 580
  - Number of spaces: 579
  - Total elements + spaces = 580 + 579 = 1159
  
  **Formula:**
  ```
  Diameter of a cone = Fovea length / (Total elements + spaces)
                     = 1.5 mm / 1159
                     = 0.00129 mm
  ```

  - The angular resolution of the eye helps calculate the smallest dot discernible at 0.2 m:
  ```
  Smallest dot = 0.00129 mm * (200 mm / 1.5 mm) = 0.0186 mm
  ```

  **Answer:** The smallest dot diameter the human eye can discern at 0.2 m is **0.0186 mm**.

---

### 3. **Visual Adaptation When Entering a Dark Theater**
- **Problem:** Why does it take time to adjust to low-light conditions when entering a dark theater from daylight?
  
  **Answer:** 
  - The delay in vision adjustment is due to **dark adaptation**, where the eye shifts from cone-based (bright light) vision to rod-based (dim light) vision.
  - Cones, responsible for color vision, function well in bright light but not in dim environments.
  - Rods, which are more sensitive in low light, take time to fully adjust, leading to a temporary period of reduced visibility until they dominate.

---

### 4. **CCD Camera Resolution**
- **Problem:** Calculate the line pairs per mm that a CCD camera can resolve.
  
  **Given:**
  - CCD camera dimensions: 7 x 7 mm
  - Number of elements: 1024 x 1024
  - Focused area distance: 0.5 m
  - Lens focal length: 35 mm

  **Steps:**
  - Element size on the sensor:
  ```
  Element size = 7 mm / 1024 = 0.006835 mm/element
  ```

  - The resolution limit in terms of line pairs per mm is determined by the element size:
  ```
  Resolution = 1 / (2 * Element size)
             = 1 / (2 * 0.006835 mm)
             = 73.14 line pairs/mm
  ```

  - Considering the lens focal length and distance, the spatial frequency can be adjusted:
  ```
  Adjusted resolution = 73.14 / 14.63 ≈ 5 line pairs/mm
  ```

  **Answer:** The camera can resolve **5 line pairs per mm**.

---

This way, the formulas are displayed properly using plain text, making the README more readable on GitHub.