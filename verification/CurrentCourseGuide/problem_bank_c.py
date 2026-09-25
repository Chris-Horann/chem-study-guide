"""Problem bank C: Chapter 1 TEXTBOOK-PREVIEW modules (t1-2 … t1-9) and the preview item in m1.
Every problem here is labeled preview. Keys are computed; verify_guide.py re-derives them."""
import math
from guide_common import *
from problem_bank_a import PROBLEMS, add, num_ans, choice, J_UNITS, M_UNITS, MS_UNITS, G_UNITS
from problem_bank_b import text_ans, formula_ans, order_ans

G_CM3_UNITS = ["g/cm3", "g/cm^3", "g/cm³", "g cm^-3", "g cm-3", "g·cm^-3", "g/ml", "g ml^-1", "g/milliliter"]
G_ML_UNITS = G_CM3_UNITS
ML_UNITS = ["ml", "milliliter", "milliliters", "millilitre", "cm3", "cm^3", "cm³"]
KM_UNITS = ["km", "kilometer", "kilometers", "kilometre", "kilometres"]
CM_UNITS = ["cm", "centimeter", "centimeters"]
KG_UNITS = ["kg", "kilogram", "kilograms"]
QT_UNITS = ["qt", "quart", "quarts"]
DEGC_UNITS = ["°c", "c", "degc", "deg c", "degrees c", "degrees celsius", "celsius", "º c", "ºc", "° c"]
K_UNITS = ["k", "kelvin", "kelvins"]
KGM3_UNITS = ["kg/m3", "kg/m^3", "kg/m³", "kg m^-3", "kg m-3"]
N_UNITS = None

def P(**kw):
    kw.setdefault("label", "preview")
    return add(**kw)

TB = "textbook"  # citation prefix
def tb(sec, pdf_from, pdf_to=None):
    if pdf_to and pdf_to != pdf_from:
        return f"textbook §{sec}, PDF p.{pdf_from}–{pdf_to} (printed {pdf_from - 34}–{pdf_to - 34})"
    return f"textbook §{sec}, PDF p.{pdf_from} (printed {pdf_from - 34})"

# =====================================================================================
# m1 preview item: scientific methods (§1.1, TB PDF p.39–40)
# =====================================================================================
P(id="m1-preview-methods", module="m1", kind="practice", level="Textbook preview",
  prompt="<p>Which statement correctly contrasts a scientific <em>law</em> with a scientific <em>theory</em>, as the textbook uses the words?</p>",
  answer=choice(("A law is a theory that has been proven.", False, "Theories never “graduate” into laws; they do different jobs."),
                ("A law describes a consistent pattern; a theory explains why the pattern happens.", True, "Right: e.g., the Law of Constant Composition describes; Dalton's atomic theory explains it."),
                ("A theory is an untested guess.", False, "That's a hypothesis. A theory has survived extensive testing."),
                ("Laws apply only to chemistry; theories apply to physics.", False, "Both terms are used across the sciences.")),
  hints=["Think of Day 1: which item <em>describes</em> (constant composition) and which <em>explains</em> (Dalton's atoms)?"],
  solution="<p>A <strong>law</strong> is a concise description of a consistent relationship; a <strong>theory</strong> is an extensively tested explanation of why it holds. A tentative explanation that hasn't been tested yet is a <strong>hypothesis</strong>. Dalton's atomic theory explains Proust's law (Day 1 p.14, covered in lecture).</p>",
  source=tb("1.1", 39, 40) + "; Day 1 p.11–14")

# =====================================================================================
# t1-2 COAST (§1.2, TB PDF p.41–42)
# =====================================================================================
P(id="t1-2-attempt", module="t1-2", kind="attempt", level="Guided attempt",
  prompt="<p>A student solves: “A cyclist rides 12.0 km in 40.0 min. What is her average speed in m/s?” Match each thing she does to the COAST step it belongs to.</p>",
  answer={"type": "match",
          "rows": [{"html": "Writes down the givens (12.0 km, 40.0 min) and notes that speed = distance ÷ time.", "answer": "C"},
                   {"html": "Notices the answer must be in m/s, so she plans to convert km → m and min → s, and estimates “about 5 m/s.”", "answer": "A"},
                   {"html": "Calculates 12,000 m ÷ 2400 s = 5.00 m/s.", "answer": "S"},
                   {"html": "Checks that 5.00 m/s is a sensible cycling speed, the units are m/s, and 3 significant figures are justified.", "answer": "T"}],
          "options": [{"key": "C", "html": "Collect and Organize"}, {"key": "A", "html": "Analyze"},
                      {"key": "S", "html": "Solve"}, {"key": "T", "html": "Think About It"}]},
  hints=["COAST names four steps: Collect and Organize, Analyze, Solve, Think About It (textbook §1.2).",
         "Collecting is gathering what's given and what's asked; Analyzing is planning how to connect them.",
         "Which action uses the units of the answer to plan the route, and includes an estimate?",
         "The final check of reasonableness, units, and sig figs is always the last step."],
  solution="<p>Givens and the relationship → <strong>Collect and Organize</strong>. Planning the unit conversions and estimating → <strong>Analyze</strong>. The arithmetic → <strong>Solve</strong>. Checking reasonableness, units, and sig figs → <strong>Think About It</strong>.</p>"
           "<p>(12.0 km × 1000 m/km) ÷ (40.0 min × 60 s/min) = 12,000 m ÷ 2400 s = 5.00 m/s.</p>",
  compare={"wrong": "<p>“COAST is a checklist: do the four steps once, in order, and never go back.”</p>",
           "tempting": "The acronym reads like a recipe.",
           "fails": "The textbook calls COAST “merely a framework for solving problems, not a recipe.” If Think About It shows the answer is unreasonable, you loop back to Analyze. It also warns against the shortcut it replaces: grabbing an equation that seems to have the right variables and plugging numbers in."},
  source=tb("1.2", 41, 42))

P(id="t1-2-p1", module="t1-2", kind="practice", level="Warm-up",
  prompt="<p>Why does the Analyze step include an order-of-magnitude (“ballpark”) estimate?</p>",
  answer=choice(("To replace the calculation when numbers are messy", False, "The estimate supplements the calculation; it doesn't replace it."),
                ("So the calculated answer can be checked against it in Think About It", True, "Right: a calculator answer far from the estimate signals a setup or entry error."),
                ("Because significant figures require it", False, "Sig figs come from the data, not from the estimate."),
                ("To decide which units to use", False, "Units come from the question; the estimate is a check.")),
  hints=["When would you compare your calculator's answer with something?"],
  solution="<p>An estimate made before calculating gives Think About It something to compare against (textbook §1.2).</p>",
  source=tb("1.2", 42))

sp = 150.0 * 1000 / (1.50 * 3600)
P(id="t1-2-p2", module="t1-2", kind="practice", level="Standard",
  prompt="<p>Estimate first, then calculate: a train travels 150. km in 1.50 h. What is its average speed in m/s?</p>",
  answer=num_ans(sp, sf=3, unit_label="m/s", units=MS_UNITS),
  hints=["Analyze: speed = distance ÷ time, and the answer must be in m/s.",
         "Estimate: 100 km/h is about 30 m/s, so expect a little under 30 m/s.",
         "150. km = 1.50 × 10<sup>5</sup> m; 1.50 h = 5400 s.",
         "Speed = 1.50 × 10<sup>5</sup> m ÷ 5400 s."],
  solution=f"<p>(150. km × 1000 m/km) ÷ (1.50 h × 3600 s/h) = <strong>{num(sp, 3)} m/s</strong>, close to the estimate, which is the Think About It check.</p>",
  source=tb("1.2", 41, 42) + "; " + tb("1.8", 60))

P(id="t1-2-p3", module="t1-2", kind="practice", level="Standard",
  prompt="<p>A student calculates that a raindrop has a mass of 4.5 kg. Which COAST step should have caught the error?</p>",
  answer=choice(("Collect and Organize", False, "Collecting the givens doesn't test the answer."), ("Analyze", False, "Analyze plans the route; the answer doesn't exist yet."),
                ("Solve", False, "Solve produced the number; it doesn't judge it."), ("Think About It", True, "Right: a 4.5 kg raindrop fails the “does this make sense?” test.")),
  hints=["Which step asks whether the answer makes sense in your own experience?"],
  solution="<p><strong>Think About It.</strong> Does the result make sense? A raindrop is a fraction of a gram, so 4.5 kg signals a units or exponent error.</p>",
  source=tb("1.2", 42))

P(id="t1-2-transfer", module="t1-2", kind="transfer", level="Transfer",
  prompt="<p>You're asked for the de Broglie wavelength of a 57.0 g ball, but λ = h/(mu) needs mass in kg. The textbook says the units of the given values and of the final answer “may help you identify how they are connected and which equation(s) may be useful”; comparing g with kg this way shows the conversion you'll need. Which COAST step is that?</p>",
  answer=choice(("Collect and Organize", False, "Recording “57.0 g” is collecting. Spotting the mismatch with the equation's units is analysis."),
                ("Analyze", True, "Right: comparing the units you have with the units the relationship needs is how you plan conversions."),
                ("Solve", False, "Discovering the mismatch mid-calculation is exactly what Analyze prevents."),
                ("Think About It", False, "That catches the error afterward, which is too late to be efficient.")),
  hints=["Collect and Organize gathers the givens and equations; one step plans the route from the givens to the answer; Solve calculates; Think About It checks."],
  solution="<p><strong>Analyze.</strong> The textbook's Analyze step: “the units of the initial values and the final answer may help you identify how they are connected” (PDF p.42, printed 8). Seeing that λ = h/(mu) needs kg (Day 4 p.11) and planning 57.0 g → 0.0570 kg happens there. Solve then makes sure the units “are consistent and cancel.”</p>",
  source=tb("1.2", 42) + "; Day 4 p.11")

P(id="t1-2-m-explain", module="t1-2", kind="mastery", level="Explain",
  prompt="<p>In your own words, what does each COAST step do, and why does the textbook call it “a framework, not a recipe”?</p>",
  answer={"type": "self", "model": "<p><strong>Collect and Organize</strong>: identify the concept, sort the relevant givens, gather needed equations and constants. <strong>Analyze</strong>: plan how to connect the givens to the answer (units help), maybe work backward, and estimate. "
                                   "<strong>Solve</strong>: carry out the plan with consistent units and appropriate sig figs. <strong>Think About It</strong>: is the answer reasonable, with correct units and sig figs, and could you solve a related problem? "
                                   "It's a framework because real problems loop: a failed check sends you back to the analysis (textbook §1.2).</p>"},
  hints=[], solution="", source=tb("1.2", 41, 42))

P(id="t1-2-m-recognize", module="t1-2", kind="mastery", level="Recognize",
  prompt="<p>Which habit does the textbook say COAST helps you avoid?</p>",
  answer=choice(("Grabbing an equation that seems to have the right variables and plugging in numbers", True, "Right: that pitfall is named explicitly in §1.2."),
                ("Using scientific notation", False, "Scientific notation is encouraged."),
                ("Estimating answers", False, "Estimating is part of Analyze."),
                ("Checking units", False, "Unit checks are part of Solve and Think About It.")),
  hints=["It's the shortcut that skips understanding."],
  solution="<p>Plugging numbers into any equation with matching symbols, or trial and error (textbook §1.2).</p>",
  source=tb("1.2", 42))

P(id="t1-2-m-sanity", module="t1-2", kind="mastery", level="Sanity check",
  prompt="<p>A classmate's estimate is “about 30 m/s,” but the calculator gives 0.083 m/s for a car's speed. What should they do?</p>",
  answer=choice(("Trust the calculator.", False, "A mismatch this large (×360) means something went wrong."),
                ("Go back to Analyze and check the conversion factors (for example, km/h ↔ m/s).", True, "Right: a factor of 3600 or 1000 usually means a flipped conversion."),
                ("Average the two answers.", False, "Averaging hides the error."),
                ("Report both.", False, "Only one can be right; find the error.")),
  hints=["A disagreement between the estimate and the result is information. What does it point to?"],
  solution="<p>Loop back: compare the units in the setup. Dividing by 3600 instead of multiplying (or the reverse) is the classic cause.</p>",
  source=tb("1.2", 42))

# =====================================================================================
# t1-3 Classes and properties of matter (§1.3, TB PDF p.42–47; Fig. 1.2 p.39)
# =====================================================================================
P(id="t1-3-attempt", module="t1-3", kind="attempt", level="Guided attempt",
  prompt="<p>Classify each sample using the textbook's scheme (Fig. 1.2).</p>",
  answer={"type": "match",
          "rows": [{"html": "neon gas inside a sign", "answer": "el"},
                   {"html": "table sugar, sucrose (C<sub>12</sub>H<sub>22</sub>O<sub>11</sub>)", "answer": "cp"},
                   {"html": "sugar completely dissolved in water (clear)", "answer": "ho"},
                   {"html": "sand stirred into water", "answer": "he"}],
          "options": [{"key": "el", "html": "element"}, {"key": "cp", "html": "compound"},
                      {"key": "ho", "html": "homogeneous mixture"}, {"key": "he", "html": "heterogeneous mixture"}]},
  hints=["First question in Fig. 1.2: can it be separated by a physical process? If yes, it's a mixture.",
         "For a pure substance: can a chemical reaction break it down into simpler substances? Yes → compound; no → element.",
         "For a mixture: is the composition uniform throughout?",
         "Sugar water can be separated by evaporating the water, and it looks the same everywhere; sand settles into a separate layer."],
  solution="<p>Neon: <strong>element</strong>. Sucrose: <strong>compound</strong> (a fixed formula; it decomposes chemically but not physically). Sugar water: <strong>homogeneous mixture</strong> (a solution: uniform, but its composition can vary and evaporation separates it). Sand in water: <strong>heterogeneous mixture</strong> (distinct regions).</p>",
  compare={"wrong": "<p>“Sugar water is a compound: it's clear and uniform, so it must be one substance.”</p>",
           "tempting": "Uniform appearance feels like “pure.”",
           "fails": "Uniform means homogeneous, not pure. Sugar water has no fixed composition (you can dissolve more or less sugar), and a physical process (evaporation) separates it. A compound has a fixed composition (constant composition, Day 1 p.11) and needs a chemical reaction to break it down."},
  source=tb("1.3", 42, 47) + "; Fig. 1.2, TB PDF p.39 (printed 5)")

P(id="t1-3-p1", module="t1-3", kind="practice", level="Warm-up",
  prompt="<p>Physical or chemical property?</p>",
  answer={"type": "match",
          "rows": [{"html": "iron rusts in moist air", "answer": "ch"}, {"html": "copper conducts electricity", "answer": "ph"},
                   {"html": "ethanol boils at 78 °C", "answer": "ph"}, {"html": "methane burns in oxygen", "answer": "ch"}],
          "options": [{"key": "ph", "html": "physical"}, {"key": "ch", "html": "chemical"}]},
  hints=["Can you observe it without turning the substance into a different substance?"],
  solution="<p>Rusting and burning change the substances (<strong>chemical</strong>). Conducting electricity and boiling leave copper and ethanol chemically the same (<strong>physical</strong>).</p>",
  source=tb("1.3", 43, 44))

P(id="t1-3-p2", module="t1-3", kind="practice", level="Warm-up",
  prompt="<p>Which property of a gold bar is <em>intensive</em>?</p>",
  answer=choice(("mass", False, "Mass depends on how much gold you have: extensive."), ("volume", False, "Extensive."),
                ("density", True, "Right: mass ÷ volume is the same for any amount of pure gold."), ("length", False, "Extensive.")),
  hints=["Intensive properties don't change when you cut the sample in half."],
  solution="<p><strong>Density.</strong> Halving the bar halves both mass and volume, so d = m/V stays the same.</p>",
  source=tb("1.3", 43))

d_al = 32.4 / 12.0
P(id="t1-3-p3", module="t1-3", kind="practice", level="Standard",
  prompt="<p>A 12.0 cm<sup>3</sup> block of metal has a mass of 32.4 g. What is its density?</p>",
  answer=num_ans(d_al, sf=3, unit_label="g/cm<sup>3</sup>", units=G_CM3_UNITS),
  hints=["d = m/V (textbook Eq. 1.1).", "Divide the mass by the volume.", "32.4 g ÷ 12.0 cm<sup>3</sup>."],
  solution=f"<p>d = 32.4 g ÷ 12.0 cm<sup>3</sup> = <strong>{num(d_al, 3)} g/cm<sup>3</sup></strong> (3 s.f.). <span class='bg'>That matches aluminum.</span></p>",
  source=tb("1.3", 43))

P(id="t1-3-p4", module="t1-3", kind="practice", level="Standard",
  prompt="<p>Choose the separation method.</p>",
  answer={"type": "match",
          "rows": [{"html": "drinking water from seawater", "answer": "di"}, {"html": "sand from water", "answer": "fi"},
                   {"html": "the colored dyes in a marker's ink", "answer": "ch"}],
          "options": [{"key": "di", "html": "distillation"}, {"key": "fi", "html": "filtration"}, {"key": "ch", "html": "chromatography"}]},
  hints=["Which difference does each method exploit: volatility, particle size, or attraction to a stationary phase?"],
  solution="<p>Seawater: <strong>distillation</strong> (water vaporizes; the salts don't). Sand: <strong>filtration</strong> (grains are bigger than the pores). Dyes: <strong>chromatography</strong> (each dye interacts differently with the stationary phase).</p>",
  source=tb("1.3", 45, 47))

V_eth = 50.0 / 0.789
P(id="t1-3-p5", module="t1-3", kind="practice", level="Standard",
  prompt="<p>Ethanol has a density of 0.789 g/mL. What volume does 50.0 g of ethanol occupy?</p>",
  answer=num_ans(V_eth, sf=3, unit_label="mL", units=ML_UNITS),
  hints=["Rearrange d = m/V for V.", "V = m/d.", "50.0 g ÷ 0.789 g/mL."],
  solution=f"<p>V = m/d = 50.0 g ÷ 0.789 g/mL = <strong>{num(V_eth, 3)} mL</strong>. Grams cancel, leaving mL.</p>",
  source=tb("1.3", 43))

P(id="t1-3-transfer", module="t1-3", kind="transfer", level="Transfer",
  prompt="<p>A clear, colorless liquid boils over a range of temperatures, and the first vapor collected has a different composition from what remains in the flask. What is the liquid?</p>",
  answer=choice(("an element", False, "A pure substance boils at one temperature and its vapor has the same composition."),
                ("a compound", False, "Also a pure substance: same composition in vapor and liquid."),
                ("a homogeneous mixture", True, "Right: uniform to the eye, but distillation partly separates its components."),
                ("a heterogeneous mixture", False, "It looked uniform (clear), so it's homogeneous.")),
  hints=["Pure substances have fixed properties. What does a changing composition tell you?", "Clear and uniform: homogeneous or heterogeneous?"],
  solution="<p>A <strong>homogeneous mixture</strong> (a solution). Distillation separates it because its components differ in volatility.</p>",
  source=tb("1.3", 44, 45))

P(id="t1-3-m-explain", module="t1-3", kind="mastery", level="Explain",
  prompt="<p>Explain, at the particle level, why distillation can separate water from dissolved salt.</p>",
  answer={"type": "self", "model": "<p>Volatility depends on how strongly the particles attract each other: the stronger the attraction, the less likely a particle escapes into the vapor. "
                                   "Water molecules can break away from the liquid at the boiling point, but Na<sup>+</sup> and Cl<sup>−</sup> ions are held very strongly and stay behind. So the vapor is nearly pure water, which condenses in a separate container (textbook §1.3).</p>"},
  hints=[], solution="", source=tb("1.3", 45))

P(id="t1-3-m-recognize", module="t1-3", kind="mastery", level="Recognize",
  prompt="<p>“A white powder decomposes when heated into a gas and a different white solid.” What does that tell you about the powder?</p>",
  answer=choice(("It's an element.", False, "Elements can't be broken down into simpler substances."), ("It's a compound (or contains one).", True, "Right: a chemical change produced simpler substances."),
                ("It's a heterogeneous mixture.", False, "Heating that produces new substances is a chemical change, not a physical separation."), ("Nothing.", False, "Decomposition is informative.")),
  hints=["Fig. 1.2: “Can it be decomposed by a chemical reaction?”"],
  solution="<p>Chemical decomposition means a <strong>compound</strong>. (This is like the Day 1 p.10 heating experiment, now read through classes of matter.)</p>",
  source=tb("1.1", 39) + "; " + tb("1.3", 43))

P(id="t1-3-m-sanity", module="t1-3", kind="mastery", level="Sanity check",
  prompt="<p>A student reports that a gold nugget has a density of 1.93 g/cm<sup>3</sup>. Gold's density is 19.3 g/cm<sup>3</sup>. What's the most likely error?</p>",
  answer=choice(("The nugget is hollow.", False, "Possible, but a factor of exactly 10 points to arithmetic."), ("A factor-of-10 slip, such as a misplaced decimal in the volume", True, "Right: exactly ×10 smells like a decimal or unit error."),
                ("Gold's density varies by sample.", False, "Density is an intensive property of pure gold."), ("Nothing; both are fine.", False, "They differ tenfold.")),
  hints=["Compare the two numbers. What's the ratio?"],
  solution="<p>The ratio is exactly 10, which points to a decimal or unit slip (e.g., 8.5 mL entered as 85 mL). Density is intensive, so a pure nugget must give 19.3 g/cm<sup>3</sup>.</p>",
  source=tb("1.3", 43))

# =====================================================================================
# t1-4 States of matter (§1.4, TB PDF p.47–50)
# =====================================================================================
P(id="t1-4-attempt", module="t1-4", kind="attempt", level="Guided attempt",
  prompt="<p>On a cold night, frost forms on a car window directly from water vapor in the air, with no liquid step. (a) Name the change. (b) Is energy absorbed or released by the water?</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) name of the change", **text_ans(["deposition"], ci=True, placeholder="one word")},
      {"label": "(b) energy", **choice(("absorbed", False, "Gas → solid moves down the energy diagram (Fig. 1.10)."), ("released", True, "Right: forming the solid releases energy."))}]},
  hints=["Identify the starting and ending states: gas → solid.", "Fig. 1.10 names six changes; which one skips the liquid on the way down?",
         "Going down Fig. 1.10 (gas → liquid → solid) releases energy; going up absorbs it.",
         "The reverse of sublimation…"],
  solution="<p>(a) <strong>Deposition</strong> (gas → solid directly; the reverse of sublimation). (b) Energy is <strong>released</strong>: molecules settle into a rigid array with less energy.</p>",
  compare={"wrong": "<p>“It's condensation, and it absorbs energy because the window is cold.”</p>",
           "tempting": "“Condensation” is the everyday word for water appearing on glass, and cold seems to mean energy is being taken in.",
           "fails": "Condensation is gas → liquid (dew). Frost skips the liquid, so it's deposition. The cold window takes energy <em>away</em> from the water molecules: the water releases energy as it forms a solid (Fig. 1.10)."},
  source=tb("1.4", 48, 49))

P(id="t1-4-p1", module="t1-4", kind="practice", level="Warm-up",
  prompt="<p>Particles are close together, randomly arranged, and slide past one another. Which state is this?</p>",
  answer=choice(("solid", False, "A solid's particles are locked in an ordered array."), ("liquid", True, "Right: close together but free to flow (Fig. 1.9b)."),
                ("gas", False, "Gas particles are far apart."), ("plasma", False, "Not part of this section.")),
  hints=["Close together rules out a gas. Ordered or not?"],
  solution="<p><strong>Liquid</strong>: little empty space, but the nearest neighbors change over time (textbook §1.4).</p>",
  source=tb("1.4", 48))

P(id="t1-4-p2", module="t1-4", kind="practice", level="Standard",
  prompt="<p>Why can a gas be compressed into a smaller volume, while a liquid essentially can't?</p>",
  answer=choice(("Gas particles are smaller.", False, "The same molecules make up water vapor and liquid water."), ("A gas is mostly empty space between particles.", True, "Right: squeezing removes empty space, not particles."),
                ("Gas particles have no mass.", False, "They have mass."), ("Liquids are always colder.", False, "Temperature isn't the point; spacing is.")),
  hints=["Compare the spacing between particles in Fig. 1.9."],
  solution="<p>The volume of the gas particles themselves is negligible compared with the volume of the gas. Compression removes empty space; in a liquid there's almost none to remove.</p>",
  source=tb("1.4", 48))

P(id="t1-4-p3", module="t1-4", kind="practice", level="Standard",
  prompt="<p>Does each change absorb or release energy?</p>",
  answer={"type": "match",
          "rows": [{"html": "ice melts", "answer": "ab"}, {"html": "water vapor condenses on a cold glass", "answer": "re"},
                   {"html": "a pond freezes", "answer": "re"}, {"html": "dry ice (solid CO<sub>2</sub>) sublimes", "answer": "ab"}],
          "options": [{"key": "ab", "html": "absorbs energy"}, {"key": "re", "html": "releases energy"}]},
  hints=["Moving toward a gas (up Fig. 1.10) absorbs energy; moving toward a solid releases it."],
  solution="<p>Melting and sublimation <strong>absorb</strong> energy; condensation and freezing <strong>release</strong> it (Fig. 1.10).</p>",
  source=tb("1.4", 48, 49))

P(id="t1-4-p4", module="t1-4", kind="practice", level="Warm-up",
  prompt="<p>Which statement describes a solid?</p>",
  answer=choice(("definite volume, no definite shape", False, "That's a liquid."), ("definite shape and definite volume", True, "Right."),
                ("neither definite shape nor volume", False, "That's a gas."), ("definite shape, no definite volume", False, "Not a real combination.")),
  hints=["Which state keeps its shape in any container?"],
  solution="<p>A solid has a <strong>definite shape and volume</strong>; a liquid has only a definite volume; a gas has neither.</p>",
  source=tb("1.4", 47))

P(id="t1-4-transfer", module="t1-4", kind="transfer", level="Transfer",
  prompt="<p>Liquid nitrogen (boiling point 77 K) is poured onto a lab bench and boils away. Why does the bench get cold?</p>",
  answer=choice(("Nitrogen molecules are cold and stick to the bench.", False, "The key is energy flow, not stickiness."),
                ("Vaporization absorbs energy, and it comes from the bench.", True, "Right: liquid → gas requires energy input."),
                ("Boiling releases energy into the bench.", False, "Vaporization absorbs energy."),
                ("Nitrogen reacts with the bench.", False, "No reaction is needed.")),
  hints=["Is liquid → gas up or down Fig. 1.10?", "Where does the energy come from?"],
  solution="<p>Vaporization moves up Fig. 1.10, so it <strong>absorbs energy</strong>. The warm bench supplies it, so the bench cools.</p>",
  source=tb("1.4", 48, 49))

P(id="t1-4-m-explain", module="t1-4", kind="mastery", level="Explain",
  prompt="<p>Explain each state's macroscopic behavior (shape, volume, compressibility) from what its particles are doing.</p>",
  answer={"type": "self", "model": "<p>Solid: particles locked in an ordered array, vibrating in place, so it keeps its shape and volume. Liquid: particles still touching but moving past one another, so the volume is fixed (little empty space) but the shape follows the container. "
                                   "Gas: particles far apart and moving freely, so a gas fills its container, and its mostly empty space can be squeezed (textbook §1.4, Fig. 1.9).</p>"},
  hints=[], solution="", source=tb("1.4", 47, 48))

P(id="t1-4-m-recognize", module="t1-4", kind="mastery", level="Recognize",
  prompt="<p>Mothballs slowly disappear in a closet without ever melting. Which change is this?</p>",
  answer=choice(("evaporation", False, "Evaporation starts from a liquid."), ("sublimation", True, "Right: solid → gas directly."), ("deposition", False, "That's gas → solid."), ("condensation", False, "That's gas → liquid.")),
  hints=["Solid → gas, skipping the liquid."],
  solution="<p><strong>Sublimation</strong>.</p>", source=tb("1.4", 48))

P(id="t1-4-m-sanity", module="t1-4", kind="mastery", level="Sanity check",
  prompt="<p>A student draws steam as molecules packed as tightly as in liquid water. What's wrong?</p>",
  answer=choice(("Nothing; the molecules are the same.", False, "Same molecules, very different spacing."), ("Gas molecules should be far apart, with mostly empty space.", True, "Right: Fig. 1.9c."),
                ("Steam molecules are larger.", False, "Molecular size doesn't change."), ("Steam should be drawn as a solid lattice.", False, "Steam is a gas.")),
  hints=["What makes a gas compressible?"],
  solution="<p>Water vapor molecules are widely separated; almost all of the volume is empty space (Fig. 1.9c).</p>",
  source=tb("1.4", 48))

# =====================================================================================
# t1-5 Forms of energy (§1.5, TB PDF p.50–51; conservation of energy = LECTURE Day 1 p.15)
# =====================================================================================
KE_bb = 0.5 * 0.145 * 40.0 ** 2
P(id="t1-5-attempt", module="t1-5", kind="attempt", level="Guided attempt",
  prompt="<p>A 145 g baseball leaves a pitcher's hand at 40.0 m/s. What is its kinetic energy in joules?</p>",
  answer=num_ans(KE_bb, sf=3, unit_label="J", units=J_UNITS, ask_unit=True),
  hints=["Energy of motion: KE = ½mu² (textbook Eq. 1.3).",
         "1 J = 1 kg·(m/s)², so mass must be in kg (textbook §1.7).",
         "145 g = 0.145 kg.",
         "KE = ½ × 0.145 kg × (40.0 m/s)²."],
  solution=f"<p>KE = ½(0.145 kg)(40.0 m/s)<sup>2</sup> = ½(0.145)(1600) kg·m<sup>2</sup>/s<sup>2</sup> = <strong>{num(KE_bb, 3)} J</strong>.</p>",
  compare={"wrong": f"<p>“KE = ½(145)(40.0)<sup>2</sup> = {num(0.5 * 145 * 1600, 3)} J”, or “KE = ½(0.145)(40.0) = 2.90 J.”</p>",
           "tempting": "Grams are the given unit, and it's easy to forget to square the speed.",
           "fails": "A joule is kg·(m/s)², so the mass must be in kg (×1000 error otherwise), and the speed is squared: doubling the speed quadruples KE (textbook §1.5)."},
  source=tb("1.5", 50, 51) + "; " + tb("1.7", 53))

P(id="t1-5-p1", module="t1-5", kind="practice", level="Warm-up",
  prompt="<p>If an object's speed triples, by what factor does its kinetic energy change?</p>",
  answer=num_ans(9, tol=0),
  hints=["KE is proportional to u².", "(3)² = ?"],
  solution="<p>KE ∝ u<sup>2</sup>, so tripling u multiplies KE by 3<sup>2</sup> = <strong>9</strong>.</p>",
  source=tb("1.5", 50))

w_ex = 25.0 * 3.00
P(id="t1-5-p2", module="t1-5", kind="practice", level="Warm-up",
  prompt="<p>You push a crate with a force of 25.0 N for 3.00 m. How much work do you do? (1 N·m = 1 J)</p>",
  answer=num_ans(w_ex, sf=3, unit_label="J", units=J_UNITS),
  hints=["w = F × d (textbook Eq. 1.2).", "25.0 N × 3.00 m."],
  solution=f"<p>w = F × d = 25.0 N × 3.00 m = <strong>{num(w_ex, 3)} J</strong>.</p>",
  source=tb("1.5", 50))

KE_e = 0.5 * ME * (2.00e6) ** 2
P(id="t1-5-p3", module="t1-5", kind="practice", level="Standard",
  prompt="<p><span class='tag-conn'>Connects to Module 5</span> An electron (m = 9.109 × 10<sup>−31</sup> kg) is ejected from a metal at 2.00 × 10<sup>6</sup> m/s. What is its kinetic energy?</p>",
  answer=num_ans(KE_e, sf=3, unit_label="J", units=J_UNITS),
  hints=["KE = ½mu².", "Square the speed: (2.00 × 10<sup>6</sup>)<sup>2</sup> = 4.00 × 10<sup>12</sup> m<sup>2</sup>/s<sup>2</sup>.", "½ × 9.109 × 10<sup>−31</sup> kg × 4.00 × 10<sup>12</sup> m<sup>2</sup>/s<sup>2</sup>."],
  solution=f"<p>KE = ½(9.109 × 10<sup>−31</sup> kg)(2.00 × 10<sup>6</sup> m/s)<sup>2</sup> = <strong>{sci(KE_e)} J</strong>, the same size as the photoelectron energies in Module 5 (KE = hν − φ, Day 3 p.19).</p>",
  source=tb("1.5", 50) + "; Day 3 p.19")

P(id="t1-5-p4", module="t1-5", kind="practice", level="Standard",
  prompt="<p>Which is an example of <em>potential</em> energy?</p>",
  answer=choice(("a sprinter running the 100 m", False, "Motion: kinetic energy."), ("the chemical energy stored in glucose", True, "Right: energy of composition (textbook §1.5)."),
                ("a thrown baseball", False, "Kinetic energy."), ("a gas molecule moving at 500 m/s", False, "Kinetic energy.")),
  hints=["Potential energy is stored because of position or composition."],
  solution="<p><strong>Chemical energy in glucose</strong>: stored in the composition of the molecules until a reaction releases it.</p>",
  source=tb("1.5", 50))

P(id="t1-5-p5", module="t1-5", kind="practice", level="Standard", label="lecture",
  prompt="<p><span class='tag-lecture'>Covered in lecture</span> A photon with more than the threshold energy strikes a metal and ejects an electron. According to the law of conservation of energy, where does the photon's “extra” energy go?</p>",
  answer=choice(("It is destroyed.", False, "Energy can't be destroyed (Day 1 p.15)."), ("It becomes the ejected electron's kinetic energy.", True, "Right: KE = hν − φ is energy bookkeeping (Day 3 p.19)."),
                ("It heats the light source.", False, "The energy was delivered to the metal's electron."), ("It turns into mass.", False, "Mass–energy conversion matters in nuclear processes, not here.")),
  hints=["Day 1 p.15: energy can't be created or destroyed, only converted. KE = hν − φ."],
  solution="<p>The part of hν beyond φ becomes the electron's <strong>kinetic energy</strong>: KE = hν − φ (Day 3 p.19). That's the law of conservation of energy in action (Day 1 p.15).</p>",
  source="Day 1 p.15; Day 3 p.19")

KE_sp = 0.5 * 60.0 * 10.0 ** 2
KE_bu = 0.5 * 0.00500 * 700.0 ** 2
P(id="t1-5-transfer", module="t1-5", kind="transfer", level="Transfer",
  prompt="<p>Which has more kinetic energy: a 60.0 kg sprinter at 10.0 m/s or a 5.00 g pellet at 700. m/s? Enter the larger KE in joules.</p>",
  answer=num_ans(max(KE_sp, KE_bu), sf=3, unit_label="J", units=J_UNITS),
  hints=["Compute both with KE = ½mu², mass in kg.", "Sprinter: ½(60.0)(10.0)<sup>2</sup>.", "Pellet: ½(0.00500)(700.)<sup>2</sup>.", "Compare."],
  solution=f"<p>Sprinter: ½(60.0 kg)(10.0 m/s)<sup>2</sup> = {num(KE_sp, 3)} J. Pellet: ½(0.00500 kg)(700. m/s)<sup>2</sup> = {num(KE_bu, 3)} J. The <strong>sprinter</strong> has more ({num(KE_sp, 3)} J): mass matters linearly, and the pellet's 70× greater speed gives only 4900× more KE per kilogram against 12,000× less mass.</p>",
  source=tb("1.5", 50))

P(id="t1-5-m-explain", module="t1-5", kind="mastery", level="Explain",
  prompt="<p>Explain the difference between potential and kinetic energy, and how the law of conservation of energy connects them.</p>",
  answer={"type": "self", "model": "<p>Potential energy is stored because of position or composition (a raised object; chemical energy in glucose). Kinetic energy is energy of motion, ½mu². "
                                   "Energy can't be created or destroyed, only converted (Day 1 p.15, covered in lecture), so stored energy released in a reaction shows up as motion, work, or heat: a sprinter converts chemical energy into kinetic energy and heat (textbook §1.5).</p>"},
  hints=[], solution="", source=tb("1.5", 50, 51) + "; Day 1 p.15")

P(id="t1-5-m-recognize", module="t1-5", kind="mastery", level="Recognize",
  prompt="<p>“Heat” in the textbook's sense is…</p>",
  answer=choice(("the temperature of an object", False, "Temperature is a property; heat is a transfer."), ("energy transferred because of a temperature difference", True, "Right (textbook §1.5)."),
                ("the kinetic energy of one molecule", False, "That's particle KE."), ("a form of potential energy", False, "Heat is a transfer of energy.")),
  hints=["It flows from warm to cool."],
  solution="<p>Heat is the <strong>transfer</strong> of energy caused by a temperature difference, from a warmer object to a cooler one.</p>",
  source=tb("1.5", 50, 51))

P(id="t1-5-m-sanity", module="t1-5", kind="mastery", level="Sanity check",
  prompt="<p>A calculation gives KE = −45 J for a moving cart. What's wrong?</p>",
  answer=choice(("Nothing; the cart moves backward.", False, "u is squared, so direction can't make KE negative."), ("KE = ½mu² can't be negative, so there's an arithmetic or sign error.", True, "Right."),
                ("The mass is negative.", False, "Mass is always positive."), ("Heat was lost.", False, "That doesn't make KE negative.")),
  hints=["What's the sign of u²?"],
  solution="<p>Both m and u<sup>2</sup> are positive, so KE ≥ 0 always.</p>",
  source=tb("1.5", 50))

# =====================================================================================
# t1-6 Formulas and models (§1.6, TB PDF p.51–53)
# =====================================================================================
P(id="t1-6-attempt", module="t1-6", kind="attempt", level="Guided attempt",
  prompt="<p>Each glucose molecule contains 6 carbon, 12 hydrogen, and 6 oxygen atoms. Write (a) its molecular formula and (b) its empirical formula.</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) molecular formula", **formula_ans(["C6H12O6"], placeholder="e.g., C2H4O2")},
      {"label": "(b) empirical formula", **formula_ans(["CH2O"], placeholder="e.g., CH2O")}]},
  hints=["A molecular formula counts the atoms in one molecule (textbook §1.6).",
         "An empirical formula gives the simplest whole-number ratio.",
         "Find the greatest common factor of 6, 12, and 6.",
         "Divide each subscript by 6."],
  solution="<p>(a) <strong>C<sub>6</sub>H<sub>12</sub>O<sub>6</sub></strong>. (b) 6 : 12 : 6 = 1 : 2 : 1 → <strong>CH<sub>2</sub>O</strong>.</p>",
  compare={"wrong": "<p>“The empirical formula is the same as the molecular formula” or “C<sub>1</sub>H<sub>2</sub>O<sub>1</sub>.”</p>",
           "tempting": "For many molecules (like water) the two are identical, and writing every subscript feels complete.",
           "fails": "The empirical formula is the <em>simplest</em> whole-number ratio, so C<sub>6</sub>H<sub>12</sub>O<sub>6</sub> reduces to CH<sub>2</sub>O. A subscript of 1 is never written (textbook §1.6; the same convention as SnO in §1.1)."},
  source=tb("1.6", 51, 52))

P(id="t1-6-p1", module="t1-6", kind="practice", level="Warm-up",
  prompt="<p>The condensed structural formula of propane is CH<sub>3</sub>CH<sub>2</sub>CH<sub>3</sub>. What is its molecular formula?</p>",
  answer=formula_ans(["C3H8"]),
  hints=["Count every C and every H in the condensed formula.", "C: 1 + 1 + 1; H: 3 + 2 + 3."],
  solution="<p>3 C and 3 + 2 + 3 = 8 H → <strong>C<sub>3</sub>H<sub>8</sub></strong>.</p>",
  source=tb("1.6", 51, 52))

P(id="t1-6-p2", module="t1-6", kind="practice", level="Warm-up",
  prompt="<p>Which element exists as diatomic molecules?</p>",
  answer=choice(("neon", False, "A noble gas: single atoms."), ("nitrogen", True, "Right: N<sub>2</sub>."), ("sodium", False, "A metal: an array of atoms."), ("carbon", False, "Not in the textbook's diatomic list.")),
  hints=["The textbook lists H<sub>2</sub>, N<sub>2</sub>, O<sub>2</sub>, F<sub>2</sub>, Cl<sub>2</sub>, Br<sub>2</sub>, I<sub>2</sub>."],
  solution="<p><strong>Nitrogen</strong>, N<sub>2</sub>. The others on the textbook's list: H<sub>2</sub>, O<sub>2</sub>, F<sub>2</sub>, Cl<sub>2</sub>, Br<sub>2</sub>, I<sub>2</sub>.</p>",
  source=tb("1.6", 51))

P(id="t1-6-p3", module="t1-6", kind="practice", level="Standard",
  prompt="<p>Why is NaCl called an empirical formula rather than a molecular formula?</p>",
  answer=choice(("Because it was discovered experimentally", False, "All formulas are determined experimentally."),
                ("Because solid NaCl is a 3-D array of ions with no molecules; the formula gives only the 1 : 1 ion ratio", True, "Right (textbook Fig. 1.17)."),
                ("Because Na and Cl are both metals", False, "Cl is a nonmetal."), ("Because the formula is too simple", False, "Simplicity isn't the criterion.")),
  hints=["Is there a “molecule” of sodium chloride?"],
  solution="<p>Ionic compounds are <strong>arrays of ions</strong>, not molecules (the lattice of Day 7 p.16). NaCl gives the simplest ratio of Na<sup>+</sup> to Cl<sup>−</sup>, 1 : 1.</p>",
  source=tb("1.6", 52) + "; Day 7 p.16")

P(id="t1-6-p4", module="t1-6", kind="practice", level="Standard",
  prompt="<p>Match each representation to what it shows best.</p>",
  answer={"type": "match",
          "rows": [{"html": "molecular formula", "answer": "count"}, {"html": "structural formula", "answer": "bonds"},
                   {"html": "ball-and-stick model", "answer": "angles"}, {"html": "space-filling model", "answer": "shape"}],
          "options": [{"key": "count", "html": "how many atoms of each element"}, {"key": "bonds", "html": "which atoms are bonded to which"},
                      {"key": "angles", "html": "3-D bond angles, clearly visible"}, {"key": "shape", "html": "overall shape, with atoms overlapping as they really do"}]},
  hints=["Fig. 1.15 shows five ways to represent acetone and acetic acid."],
  solution="<p>Molecular formula → counts; structural formula → connectivity; ball-and-stick → bond angles (atoms look too far apart); space-filling → realistic overall shape (some atoms hidden).</p>",
  source=tb("1.6", 51, 52))

P(id="t1-6-transfer", module="t1-6", kind="transfer", level="Transfer",
  prompt="<p>Hydrogen peroxide (Day 1 p.13) has the molecular formula H<sub>2</sub>O<sub>2</sub>. What is its empirical formula?</p>",
  answer=formula_ans(["HO"], placeholder="e.g., CH2O"),
  hints=["Divide both subscripts by their greatest common factor.", "2 : 2 = 1 : 1."],
  solution="<p>H<sub>2</sub>O<sub>2</sub> → 1 : 1 → <strong>HO</strong>. Water, H<sub>2</sub>O, is already in lowest terms. Two compounds can share an empirical formula only if their ratios match, and these don't: that's why they illustrate multiple proportions (Day 1 p.13).</p>",
  source=tb("1.6", 52) + "; Day 1 p.13")

P(id="t1-6-m-explain", module="t1-6", kind="mastery", level="Explain",
  prompt="<p>What information does a molecular formula give that an empirical formula may not, and what does neither one show?</p>",
  answer={"type": "self", "model": "<p>A molecular formula gives the actual number of each atom in one molecule (C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>); an empirical formula gives only the simplest ratio (CH<sub>2</sub>O), which many different compounds can share. "
                                   "Neither shows which atoms are bonded to which or the 3-D shape; structural formulas and models do that (textbook §1.6).</p>"},
  hints=[], solution="", source=tb("1.6", 51, 52))

P(id="t1-6-m-recognize", module="t1-6", kind="mastery", level="Recognize",
  prompt="<p>You need to see the angles between bonds clearly. Which representation?</p>",
  answer=choice(("molecular formula", False, "No geometry."), ("condensed structural formula", False, "Connectivity, not angles."),
                ("ball-and-stick model", True, "Right."), ("empirical formula", False, "Only a ratio.")),
  hints=["Sticks make the angles easy to see."],
  solution="<p><strong>Ball-and-stick</strong>: accurate bond angles, although the atoms look farther apart than they are.</p>",
  source=tb("1.6", 51, 52))

P(id="t1-6-m-sanity", module="t1-6", kind="mastery", level="Sanity check",
  prompt="<p>A student says the empirical formula of benzene, C<sub>6</sub>H<sub>6</sub>, is C<sub>6</sub>H<sub>6</sub>. Right?</p>",
  answer=choice(("Yes", False, "6 : 6 reduces."), ("No; it's CH.", True, "Right: 6 : 6 = 1 : 1."), ("No; it's C<sub>3</sub>H<sub>3</sub>.", False, "Not fully reduced."), ("No; it's C<sub>2</sub>H<sub>2</sub>.", False, "Not fully reduced.")),
  hints=["Reduce 6 : 6 completely."],
  solution="<p><strong>CH</strong>. (Acetylene, C<sub>2</sub>H<sub>2</sub>, has the same empirical formula.)</p>",
  source=tb("1.6", 52))

# =====================================================================================
# t1-7 Measurement: units, precision, significant figures (§1.7, TB PDF p.53–60)
# =====================================================================================
m_liq = 57.9 - 42.37
d_liq = m_liq / 15.25
P(id="t1-7-attempt", module="t1-7", kind="attempt", level="Guided attempt",
  prompt="<p>An empty beaker has a mass of 42.37 g. With a liquid in it, the mass is 57.9 g. The liquid's volume is 15.25 mL. What is the liquid's density, with the correct number of significant figures?</p>",
  answer=num_ans(d_liq, sf=3, unit_label="g/mL", units=G_ML_UNITS),
  hints=["Two steps: a subtraction (mass of liquid), then a division (density).",
         "Subtraction keeps the fewest decimal places: 57.9 (one decimal place) − 42.37 → the result is known to 0.1 g.",
         "Mass of liquid = 15.53 g, known only to ±0.1 g, so it has 3 significant figures (15.5). Keep the extra digit until the end.",
         "d = 15.53 g ÷ 15.25 mL; the weak link is 3 significant figures."],
  solution=f"<p>Mass of liquid = 57.9 g − 42.37 g = {fix(m_liq, 2)} g, known to the tenths place, so <strong>3</strong> significant figures. "
           f"d = {fix(m_liq, 2)} g ÷ 15.25 mL = {fix(d_liq, 4)} g/mL → <strong>{fix(d_liq, 2)} g/mL</strong> (3 s.f.: the mass is the weak link). Round only at the end.</p>",
  compare={"wrong": f"<p>“15.53 has 4 significant figures and 15.25 has 4, so d = {fix(d_liq, 3)} g/mL.”</p>",
           "tempting": "The calculator shows 15.53, which looks like 4 significant figures.",
           "fails": "In a subtraction the limit is decimal places, not significant figures: 57.9 is known only to 0.1 g, so the difference is too. That leaves 3 significant figures for the division (the textbook's weak-link principle)."},
  source=tb("1.7", 58, 60))

P(id="t1-7-p1", module="t1-7", kind="practice", level="Warm-up",
  prompt="<p>How many significant figures are in each value?</p>",
  answer={"type": "multi", "parts": [
      {"label": "0.0592 g", **num_ans(3, tol=0)}, {"label": "3.00 × 10<sup>8</sup> m/s", **num_ans(3, tol=0)},
      {"label": "101.3 kPa", **num_ans(4, tol=0)}, {"label": "0.07010 L", **num_ans(4, tol=0)}]},
  hints=["Leading zeros never count; zeros between nonzero digits always count.", "Trailing zeros after a decimal point count."],
  solution="<p>0.0592 → <strong>3</strong> (leading zeros only place the decimal). 3.00 × 10<sup>8</sup> → <strong>3</strong>. 101.3 → <strong>4</strong> (captive zero). 0.07010 → <strong>4</strong> (7, 0, 1, and the final 0).</p>",
  source=tb("1.7", 57))

P(id="t1-7-p2", module="t1-7", kind="practice", level="Standard",
  prompt="<p>Using the textbook's tie-breaking rule, round 76.45 to three significant figures.</p>",
  answer=num_ans(76.4, tol=0),
  hints=["The first dropped digit is exactly 5 with nothing after it: a tie.", "The textbook breaks ties by rounding to the nearest even digit."],
  solution="<p><strong>76.4</strong>: the tenths digit 4 is already even. (76.55 would round to 76.6.) This is the textbook's convention; the lecture hasn't stated a rounding policy.</p>",
  source=tb("1.7", 57, 58))

P(id="t1-7-p3", module="t1-7", kind="practice", level="Warm-up",
  prompt="<p>Which value is exact (no uncertainty)?</p>",
  answer=choice(("the 1.80 × 10<sup>−10</sup> m wavelength from Day 4 p.12", False, "Calculated from measured values."), ("the 12 eggs in a carton", True, "Right: counted."),
                ("the 2.998 × 10<sup>8</sup> m/s used for c", False, "A rounded value with 4 significant figures."), ("the 0.142 kg mass of a baseball", False, "Measured.")),
  hints=["Exact numbers come from counting or from definitions."],
  solution="<p>Counted quantities (12 eggs) are <strong>exact</strong> and never limit significant figures.</p>",
  source=tb("1.7", 55))

P(id="t1-7-p4", module="t1-7", kind="practice", level="Standard",
  prompt="<p>A standard mass is exactly 10.000 g. Balance A reads 10.52, 10.51, 10.53 g; balance B reads 9.8, 10.3, 10.0 g. Which description fits?</p>",
  answer=choice(("A is precise but not accurate; B's average is closer to the true value but its readings are less precise.", True, "Right: A clusters tightly around the wrong value."),
                ("A is accurate and precise.", False, "A's readings are all about 0.5 g too high."), ("B is precise but not accurate.", False, "B scatters widely."),
                ("Both are equally accurate.", False, "Compare each average with 10.000 g.")),
  hints=["Precision = agreement among repeats. Accuracy = closeness to the true value."],
  solution="<p>A: tight cluster (precise) around 10.52 g (not accurate). B: average 10.03 g (close to true), but spread over 0.5 g (less precise). Fig. 1.22's darts show the same distinction.</p>",
  source=tb("1.7", 55, 56))

s_add = 18.2 + 0.456 + 3.12
P(id="t1-7-p5", module="t1-7", kind="practice", level="Standard",
  prompt="<p>Add these measured lengths and report the sum correctly: 18.2 m + 0.456 m + 3.12 m.</p>",
  answer=num_ans(s_add, sf=3, unit_label="m", units=M_UNITS),
  hints=["For addition, find the value with the fewest digits after the decimal point.", "18.2 has one decimal place, so the sum is reported to the tenths place."],
  solution=f"<p>Sum = {fix(s_add, 3)} m → <strong>{fix(s_add, 1)} m</strong> (tenths place, set by 18.2).</p>",
  source=tb("1.7", 58))

avg3 = (2.51 + 2.49 + 2.52) / 3
P(id="t1-7-transfer", module="t1-7", kind="transfer", level="Transfer",
  prompt="<p>Three measurements of a coin's diameter are 2.51, 2.49, and 2.52 cm. Report their average with the correct number of significant figures.</p>",
  answer=num_ans(avg3, sf=3, unit_label="cm", units=CM_UNITS),
  hints=["First add, then divide by 3.", "The sum 7.52 cm is known to the hundredths place (3 s.f.).", "3 is an exact count, so it doesn't limit the result."],
  solution=f"<p>(2.51 + 2.49 + 2.52) cm = 7.52 cm (3 s.f.); 7.52 cm ÷ 3 (exact) = {fix(avg3, 4)} → <strong>{fix(avg3, 2)} cm</strong>.</p>",
  source=tb("1.7", 58, 59))

P(id="t1-7-m-explain", module="t1-7", kind="mastery", level="Explain",
  prompt="<p>State the textbook's two weak-link rules and explain why they differ for × ÷ and for + −.</p>",
  answer={"type": "self", "model": "<p>Multiplying or dividing: the result has as many significant figures as the least certain input, because relative uncertainty carries through a product. "
                                   "Adding or subtracting: the result has as many decimal places as the input with the fewest, because absolute uncertainty in a given place carries through a sum (an uncertainty of ±0.1 g stays ±0.1 g). "
                                   "Either way, you can know a result only as well as the least well-known value (textbook §1.7).</p>"},
  hints=[], solution="", source=tb("1.7", 58))

P(id="t1-7-m-recognize", module="t1-7", kind="mastery", level="Recognize",
  prompt="<p>A calculation is 6.626 × 10<sup>−34</sup> J·s × 5.7 × 10<sup>14</sup> s<sup>−1</sup>. How many significant figures should the answer have?</p>",
  answer=choice(("2", True, "Right: 5.7 has 2 s.f., the weak link in a product."), ("3", False, "Count the digits in 5.7."), ("4", False, "6.626 has 4, but the weak link rules."), ("6", False, "Significant figures don't add.")),
  hints=["It's a multiplication: count significant figures, not decimal places."],
  solution="<p><strong>2</strong>. The weak link is 5.7 × 10<sup>14</sup> (2 s.f.).</p>",
  source=tb("1.7", 58))

P(id="t1-7-m-sanity", module="t1-7", kind="mastery", level="Sanity check",
  prompt="<p>A lab report gives a density as 2.718281 g/mL, calculated from a mass of 4.3 g. What's the problem?</p>",
  answer=choice(("Nothing; more digits are more accurate.", False, "Extra digits claim precision the data don't have."), ("Too many significant figures: 4.3 g limits the result to 2 (2.7 g/mL).", True, "Right."),
                ("It should be in kg/L.", False, "Units are fine."), ("Density must be a whole number.", False, "No.")),
  hints=["What's the weak link?"],
  solution="<p>With a mass of only 2 s.f., report <strong>2.7 g/mL</strong>.</p>",
  source=tb("1.7", 58))

# =====================================================================================
# t1-8 Unit conversions and dimensional analysis (§1.8, TB PDF p.60–65)
# =====================================================================================
km_mar = 26.2 / MI_PER_KM
P(id="t1-8-attempt", module="t1-8", kind="attempt", level="Guided attempt",
  prompt="<p>A marathon is 26.2 miles. How long is it in kilometers? (Table 1.3: 1 km = 0.6214 mi.)</p>",
  answer=num_ans(km_mar, sf=3, unit_label="km", units=KM_UNITS, ask_unit=True),
  hints=["Dimensional analysis: multiply by a conversion factor written so the unwanted unit cancels (textbook Eq. 1.4).",
         "The two possible factors are (1 km / 0.6214 mi) and (0.6214 mi / 1 km).",
         "You start with miles, so miles must be in the denominator.",
         "26.2 mi × (1 km / 0.6214 mi)."],
  solution=f"<p>26.2 mi × (1 km / 0.6214 mi) = <strong>{num(km_mar, 3)} km</strong>. Miles cancel. Sanity check: a kilometer is shorter than a mile, so the number of km must be larger.</p>",
  compare={"wrong": f"<p>“26.2 × 0.6214 = {num(26.2 * MI_PER_KM, 3)} km.”</p>",
           "tempting": "Multiplying by the number in the equivalence feels natural.",
           "fails": "Written out with units, 26.2 mi × 0.6214 mi/km gives mi²/km: the units don't cancel, which signals the wrong factor. And 16.3 km is shorter than 26.2 mi, impossible since 1 km < 1 mi."},
  source=tb("1.8", 61) + "; Table 1.3, " + tb("1.7", 54))

cm5 = 5.00 * CM_PER_IN
P(id="t1-8-p1", module="t1-8", kind="practice", level="Warm-up",
  prompt="<p>Convert 5.00 in to centimeters (1 in = 2.54 cm, exactly).</p>",
  answer=num_ans(cm5, sf=3, unit_label="cm", units=CM_UNITS),
  hints=["Put inches in the denominator of the factor.", "5.00 in × (2.54 cm / 1 in)."],
  solution=f"<p>5.00 in × (2.54 cm/1 in) = <strong>{num(cm5, 3)} cm</strong>. The exact factor doesn't limit sig figs; 5.00 sets 3.</p>",
  source=tb("1.8", 61) + "; Table 1.3, " + tb("1.7", 54))

qt = 0.355 * QT_PER_L
P(id="t1-8-p2", module="t1-8", kind="practice", level="Standard",
  prompt="<p>A can holds 355 mL. How many quarts is that? (1 L = 1.057 qt.)</p>",
  answer=num_ans(qt, sf=3, unit_label="qt", units=QT_UNITS),
  hints=["Two factors: mL → L, then L → qt.", "355 mL × (1 L / 1000 mL) × (1.057 qt / 1 L)."],
  solution=f"<p>355 mL × (1 L/1000 mL) × (1.057 qt/1 L) = <strong>{num(qt, 3)} qt</strong>.</p>",
  source=tb("1.8", 61) + "; Table 1.3, " + tb("1.7", 54))

tC = (98.6 - 32) * 5 / 9
tK = tC + 273.15
P(id="t1-8-p3", module="t1-8", kind="practice", level="Standard",
  prompt="<p>Normal body temperature is 98.6 °F. Express it in (a) °C and (b) K.</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) °C", **num_ans(tC, sf=3, tol=0.002, unit_label="°C")},
      {"label": "(b) K", **num_ans(tK, sf=4, tol=0.0005, unit_label="K")}]},
  hints=["T(°C) = (5/9)[T(°F) − 32] (Table 1.3).", "(5/9)(98.6 − 32) = (5/9)(66.6).", "T(K) = T(°C) + 273.15."],
  solution=f"<p>(a) (5/9)(98.6 − 32) = <strong>{fix(tC, 1)} °C</strong>. (b) {fix(tC, 1)} + 273.15 = 310.15 → <strong>310.2 K</strong>: addition keeps one decimal place (set by 37.0), and the dropped digit is exactly 5, so the textbook's rule rounds to the even digit, which here means rounding up (§1.7). Kelvin and Celsius degrees are the same size; only the zero points differ.</p>",
  source=tb("1.8", 64) + "; Table 1.3, " + tb("1.7", 54))

d_Au_si = 19.3 * 1e-3 * 1e6
P(id="t1-8-p4", module="t1-8", kind="practice", level="Stretch",
  prompt="<p>Gold's density is 19.3 g/cm<sup>3</sup>. Express it in kg/m<sup>3</sup>.</p>",
  answer=num_ans(d_Au_si, sf=3, unit_label="kg/m<sup>3</sup>", units=KGM3_UNITS),
  hints=["Convert the numerator and the denominator separately.", "g → kg: × (1 kg/1000 g).", "cm<sup>3</sup> → m<sup>3</sup>: cube the length factor: (100 cm/1 m)<sup>3</sup> = 10<sup>6</sup> cm<sup>3</sup>/m<sup>3</sup>.", "19.3 × 10<sup>−3</sup> × 10<sup>6</sup>."],
  solution=f"<p>19.3 g/cm<sup>3</sup> × (1 kg/1000 g) × (10<sup>6</sup> cm<sup>3</sup>/1 m<sup>3</sup>) = <strong>{sci(d_Au_si)} kg/m<sup>3</sup></strong>. Volume factors are cubed length factors (textbook Sample Exercise 1.8 cubes them the same way).</p>",
  source=tb("1.8", 63))

m_hg = 250. * 13.6 / 1000
P(id="t1-8-transfer", module="t1-8", kind="transfer", level="Transfer",
  prompt="<p>What is the mass, in kilograms, of 250. mL of mercury (density 13.6 g/cm<sup>3</sup>)? (1 mL = 1 cm<sup>3</sup>.)</p>",
  answer=num_ans(m_hg, sf=3, unit_label="kg", units=KG_UNITS),
  hints=["Density is itself a conversion factor between volume and mass.", "250. mL × (13.6 g / 1 mL).", "Then g → kg."],
  solution=f"<p>250. mL × (13.6 g/1 mL) × (1 kg/1000 g) = <strong>{num(m_hg, 3)} kg</strong>, a heavy flask for its size.</p>",
  source=tb("1.8", 61))

P(id="t1-8-m-explain", module="t1-8", kind="mastery", level="Explain",
  prompt="<p>Why doesn't multiplying by a conversion factor change the quantity, and how do the units tell you whether you set it up correctly?</p>",
  answer={"type": "self", "model": "<p>A conversion factor's numerator and denominator are equal quantities (1 km = 0.6214 mi), so the factor equals 1: the quantity is unchanged and only its units change. "
                                   "Write every unit: if the starting unit cancels and the desired one remains, the setup is right; leftover or squared units mean a flipped factor (textbook Eq. 1.4).</p>"},
  hints=[], solution="", source=tb("1.8", 61))

P(id="t1-8-m-recognize", module="t1-8", kind="mastery", level="Recognize",
  prompt="<p>You know a liquid's volume and need its mass. Which quantity is the conversion factor?</p>",
  answer=choice(("its temperature", False, "Temperature doesn't convert volume to mass."), ("its density", True, "Right: d = m/V links them."),
                ("its boiling point", False, "Not a conversion factor."), ("the speed of light", False, "Unrelated.")),
  hints=["Which ratio has mass over volume?"],
  solution="<p><strong>Density</strong> (mass per volume). Its reciprocal converts mass back to volume.</p>",
  source=tb("1.8", 61))

P(id="t1-8-m-sanity", module="t1-8", kind="mastery", level="Sanity check",
  prompt="<p>A student converts 5.0 m to cm and gets 0.050 cm. Plausible?</p>",
  answer=choice(("Yes", False, "A centimeter is smaller than a meter, so there must be more of them."), ("No: it should be 5.0 × 10<sup>2</sup> cm; the factor was flipped.", True, "Right."),
                ("No: it should be 50 cm.", False, "1 m = 100 cm."), ("Yes, if the metre stick is short.", False, "Units don't depend on the stick.")),
  hints=["Smaller unit → bigger number."],
  solution="<p>5.0 m × (100 cm/1 m) = <strong>5.0 × 10<sup>2</sup> cm</strong>.</p>",
  source=tb("1.8", 61))

# =====================================================================================
# t1-9 Analyzing experimental results (§1.9, TB PDF p.65–71)
# =====================================================================================
data_a = [12.3, 12.6, 12.4, 12.5, 12.7]
ma, sa = mean(data_a), stdev(data_a)
ci_a = T_TABLE[len(data_a) - 1][1] * sa / math.sqrt(len(data_a))
s_wrong = math.sqrt(sum((x - ma) ** 2 for x in data_a) / len(data_a))
P(id="t1-9-attempt", module="t1-9", kind="attempt", level="Guided attempt",
  prompt="<p>Five analyses of a water sample give 12.3, 12.6, 12.4, 12.5, and 12.7 mg/L. Find (a) the mean, (b) the standard deviation s, and (c) the half-width of the 95% confidence interval (t = 2.776 for n − 1 = 4, Table 1.5).</p>",
  answer={"type": "multi", "parts": [
      {"label": "(a) mean (mg/L)", **num_ans(ma, sf=4, tol=0.001)},
      {"label": "(b) s (mg/L)", **num_ans(sa, sf=2, tol=0.02)},
      {"label": "(c) 95% half-width ts/√n (mg/L)", **num_ans(ci_a, sf=2, tol=0.02)}]},
  hints=["Mean: x̄ = Σx<sub>i</sub>/n (Eq. 1.5).",
         "Deviations from 12.50: −0.2, +0.1, −0.1, 0.0, +0.2. Square them and add: 0.10.",
         "s = √[Σ(x<sub>i</sub> − x̄)<sup>2</sup>/(n − 1)] (Eq. 1.6) = √(0.10/4).",
         "Half-width = t·s/√n (Eq. 1.7) = 2.776 × s/√5."],
  solution=f"<p>(a) x̄ = 62.5/5 = <strong>{fix(ma, 2)} mg/L</strong>. (b) Σ(x<sub>i</sub> − x̄)<sup>2</sup> = 0.10; s = √(0.10/4) = <strong>{fix(sa, 2)} mg/L</strong>. "
           f"(c) ts/√n = 2.776 × {fix(sa, 3)}/√5 = <strong>{fix(ci_a, 2)} mg/L</strong>, so μ = {fix(ma, 2)} ± {fix(ci_a, 2)} mg/L at 95% confidence.</p>",
  compare={"wrong": f"<p>“s = √(0.10/5) = {fix(s_wrong, 3)} mg/L.”</p>",
           "tempting": "Dividing by n looks like “the average of the squared deviations.”",
           "fails": "The textbook's Eq. 1.6 divides by n − 1, which accounts for the mean having been calculated from the same data. With few measurements the difference matters: 0.141 vs. 0.158."},
  source=tb("1.9", 65, 68))

data_b = [2.31, 2.35, 2.29, 2.33]
P(id="t1-9-p1", module="t1-9", kind="practice", level="Warm-up",
  prompt="<p>Find the mean of 2.31, 2.35, 2.29, and 2.33 g.</p>",
  answer=num_ans(mean(data_b), sf=3, unit_label="g", units=G_UNITS),
  hints=["Add the values, then divide by the number of values.", "Sum = 9.28 g; n = 4."],
  solution=f"<p>x̄ = 9.28 g / 4 = <strong>{fix(mean(data_b), 2)} g</strong>.</p>",
  source=tb("1.9", 66))

data_c = [10.1, 10.3, 10.2]
P(id="t1-9-p2", module="t1-9", kind="practice", level="Standard",
  prompt="<p>Find the standard deviation of 10.1, 10.3, and 10.2 mL.</p>",
  answer=num_ans(stdev(data_c), sf=1, tol=0.02, unit_label="mL", units=ML_UNITS),
  hints=["Mean = 10.2 mL.", "Deviations: −0.1, +0.1, 0.0 → squares 0.01, 0.01, 0.", "s = √(0.02/(3 − 1))."],
  solution=f"<p>s = √(0.02/2) = <strong>{fix(stdev(data_c), 1)} mL</strong>.</p>",
  source=tb("1.9", 66))

ci_c = T_TABLE[5][1] * 0.12 / math.sqrt(6)
P(id="t1-9-p3", module="t1-9", kind="practice", level="Standard",
  prompt="<p>Six measurements have x̄ = 8.24 ppm and s = 0.12 ppm. What is the half-width of the 95% confidence interval? (Table 1.5: t = 2.571 for n − 1 = 5.)</p>",
  answer=num_ans(ci_c, sf=2, tol=0.04),
  hints=["Half-width = t·s/√n.", "2.571 × 0.12 / √6."],
  solution=f"<p>2.571 × 0.12/√6 = <strong>{fix(ci_c, 2)} ppm</strong>, so μ = 8.24 ± {fix(ci_c, 2)} ppm (95%).</p>",
  source=tb("1.9", 67))

data_g = [5.02, 5.05, 5.03, 5.04, 5.21]
mg_, sg_ = mean(data_g), stdev(data_g)
Zg = abs(5.21 - mg_) / sg_
P(id="t1-9-p4", module="t1-9", kind="practice", level="Stretch",
  prompt="<p>Data: 5.02, 5.05, 5.03, 5.04, and 5.21 g. Calculate Grubbs' Z for the suspect value 5.21 g (use the mean and s of all five values). Is it an outlier at 95% confidence (reference Z = 1.715 for n = 5, Table 1.7)?</p>",
  answer={"type": "multi", "parts": [
      {"label": "Z", **num_ans(Zg, sf=3, tol=0.02)},
      {"label": "outlier at 95%?", **choice(("yes", Zg > GRUBBS_Z[5][0], "Compare Z with 1.715."), ("no", Zg <= GRUBBS_Z[5][0], "Compare Z with 1.715."))}]},
  hints=["Z = |x<sub>i</sub> − x̄|/s (Eq. 1.8).", f"x̄ = {fix(mg_, 3)} g; s = {fix(sg_, 4)} g.", "Z = |5.21 − x̄|/s.", "Outlier if Z > 1.715."],
  solution=f"<p>x̄ = {fix(mg_, 3)} g, s = {fix(sg_, 4)} g. Z = |5.21 − {fix(mg_, 3)}|/{fix(sg_, 4)} = <strong>{fix(Zg, 2)}</strong> {'>' if Zg > 1.715 else '≤'} 1.715, so it <strong>{'is' if Zg > 1.715 else 'is not'}</strong> an outlier at 95% confidence. Grubbs' test may be applied only once to a data set (textbook §1.9).</p>",
  source=tb("1.9", 69, 70))

P(id="t1-9-p5", module="t1-9", kind="practice", level="Warm-up",
  prompt="<p>For normally distributed data, about what fraction of values lie within one standard deviation of the mean?</p>",
  answer=choice(("50%", False, "Too few."), ("68%", True, "Right (textbook Fig. 1.29)."), ("95%", False, "That's about two standard deviations."), ("100%", False, "Some values always fall outside.")),
  hints=["The shaded region of the bell curve in Fig. 1.29."],
  solution="<p>About <strong>68%</strong>.</p>", source=tb("1.9", 68))

data_t = dict(mean=4.62, s=0.05, n=4, true=4.50)
ci_t = T_TABLE[3][1] * 0.05 / math.sqrt(4)
P(id="t1-9-transfer", module="t1-9", kind="transfer", level="Transfer",
  prompt="<p>A control sample is known to contain 4.50 mg/dL. Four analyses give x̄ = 4.62 mg/dL and s = 0.05 mg/dL. Using the 95% confidence interval (t = 3.182 for n − 1 = 3), are the analyses accurate?</p>",
  answer=choice(("Yes: the interval contains 4.50.", 4.62 - ci_t <= 4.50 <= 4.62 + ci_t, "Check the interval's endpoints."),
                ("No: the interval, about 4.54 to 4.70, does not contain 4.50.", not (4.62 - ci_t <= 4.50 <= 4.62 + ci_t), "Right: the true value lies outside the 95% interval."),
                ("Can't tell without more data.", False, "The interval gives a decision."), ("Yes, because s is small.", False, "Small s means precise, not accurate.")),
  hints=["μ = x̄ ± ts/√n.", f"Half-width = 3.182 × 0.05/√4 = {fix(ci_t, 3)}.", "Does the interval include the known value?"],
  solution=f"<p>Half-width = 3.182 × 0.05/2 = {fix(ci_t, 3)} mg/dL, so μ = {fix(4.62 - ci_t, 2)} to {fix(4.62 + ci_t, 2)} mg/dL. The known 4.50 lies outside, so the analyses are <strong>precise but not accurate</strong> (systematically high).</p>",
  source=tb("1.9", 67))

P(id="t1-9-m-explain", module="t1-9", kind="mastery", level="Explain",
  prompt="<p>What does the standard deviation tell you, and what does the confidence interval add?</p>",
  answer={"type": "self", "model": "<p>s measures the spread of repeated results (precision): a smaller s means tighter clustering. "
                                   "The confidence interval uses s, n, and t to give a range that probably (e.g., 95%) contains the true mean, which lets you judge accuracy: if a known value falls outside, the method is biased. "
                                   "More measurements (larger n) narrow the interval (textbook §1.9).</p>"},
  hints=[], solution="", source=tb("1.9", 66, 67))

P(id="t1-9-m-recognize", module="t1-9", kind="mastery", level="Recognize",
  prompt="<p>One of your ten readings looks suspiciously high. Which tool decides whether you may discard it?</p>",
  answer=choice(("the mean", False, "The mean includes the suspect value."), ("Grubbs' test", True, "Right: Z = |x<sub>i</sub> − x̄|/s compared with Table 1.7."),
                ("the confidence interval", False, "That judges accuracy, not single points."), ("just drop it", False, "The textbook calls discarding data without a valid reason unethical.")),
  hints=["Z = |x<sub>i</sub> − x̄|/s."],
  solution="<p><strong>Grubbs' test</strong>, once per data set.</p>", source=tb("1.9", 68, 69))

P(id="t1-9-m-sanity", module="t1-9", kind="mastery", level="Sanity check",
  prompt="<p>A student reports s = −0.03 g. What's wrong?</p>",
  answer=choice(("Nothing: negative means below the mean.", False, "s is a square root of squared deviations."), ("s can never be negative.", True, "Right."),
                ("s must be larger than the mean.", False, "No."), ("s must be a whole number.", False, "No.")),
  hints=["Look at Eq. 1.6: what does a square root of a sum of squares give?"],
  solution="<p>s = √[Σ(x<sub>i</sub> − x̄)<sup>2</sup>/(n − 1)] is always ≥ 0.</p>", source=tb("1.9", 66))
