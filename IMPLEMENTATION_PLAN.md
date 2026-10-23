# ThreatScope AI - 7-Day Implementation Plan

**Goal**: Build an operational threat intelligence research tool for 10a Labs Research Fellow application

**Timeline**: 7 days (can be compressed or extended)

---

## Day 1: Research Framework & Data Collection Setup

### Objectives
- ✅ Define threat taxonomy (DONE - using FIST + MITRE F3)
- ✅ Set up project structure (DONE)
- ✅ Implement data collection pipeline (DONE)

### Tasks

**1.1 Configure APIs**
- [ ] Create Anthropic API key (free tier available)
- [ ] Create Reddit app at reddit.com/prefs/apps
- [ ] Copy `.env.example` to `.env` and fill in credentials
- [ ] Test API connections

**1.2 Database Setup**
- [ ] Run initial data collection to test database
```bash
python -c "from database import init_db; init_db(); print('✓ Database initialized')"
```

**1.3 Collect Sample Data**
- [ ] Run collectors to pull initial data
```bash
python -c "from collectors import collect_all_sources; posts = collect_all_sources(reddit=True, rss=True); print(f'Collected {len(posts)} posts')"
```

### Deliverables
- [ ] `.env` file with valid API keys
- [ ] `threatscope.db` with 100+ posts collected
- [ ] Verified collectors working for Reddit + RSS

### Time Estimate: 1-2 hours

---

## Day 2: Threat Classification Development

### Objectives
- ✅ Build LLM classifier (DONE - basic implementation)
- Refine threat prompts
- Test on sample posts

### Tasks

**2.1 Test Classifier**
```bash
# Test classification on a sample post
python -c "
from classifier import classify_post

post = '''
Just got an offer from TechCorp recruiter on LinkedIn. 
Interview was via weird AI video platform, they asked for my SSN during first call.
They said I'd start making $200k but need to pay $500 setup fee first. 
Feels off...
'''

result = classify_post(post, platform='reddit', author='test_user')
print(result)
"
```

**2.2 Classify Collected Posts**
- [ ] Run batch classification on 50-100 posts
- [ ] Review classifications for accuracy
- [ ] Refine threat detection prompts based on results

**2.3 Implement Confidence Scoring**
- [ ] Verify HIGH/MEDIUM/LOW confidence assignments
- [ ] Extract signals from each classification
- [ ] Store in database with reasoning

### Deliverables
- [ ] 50+ classified posts in database
- [ ] Sample classifications reviewed for accuracy
- [ ] Prompt refinements documented

### Time Estimate: 2-3 hours

---

## Day 3: Database & Validation Framework

### Objectives
- ✅ Database schema in place (DONE)
- Build validation workflow
- Implement signal extraction

### Tasks

**3.1 Manual Validation Process**
- [ ] Create script to review high-confidence findings
- [ ] Implement marking findings as "verified" or "false positive"
- [ ] Build validation metrics (precision, recall estimation)

**3.2 Extract & Store Signals**
- [ ] Parse signals from classifier output
- [ ] Store signals in database with evidence links
- [ ] Create utility to view signals for each finding

**3.3 Generate Statistics**
```bash
# Test statistics function
python -c "
from database import get_statistics
stats = get_statistics()
print(f'Total posts: {stats[\"total_posts\"]}')
print(f'By category: {stats[\"by_category\"]}')
print(f'By severity: {stats[\"by_severity\"]}')
"
```

### Deliverables
- [ ] Validation workflow documented
- [ ] Signal extraction working
- [ ] Statistics generation functional

### Time Estimate: 2 hours

---

## Day 4: Dashboard Development

### Objectives
- ✅ Streamlit dashboard created (DONE - basic version)
- Add visualizations
- Test interactive features

### Tasks

**4.1 Verify Dashboard**
```bash
streamlit run dashboard.py
```

**4.2 Dashboard Features to Test**
- [ ] Overview metrics display
- [ ] Threat findings filtering (category, severity, confidence)
- [ ] Chart generation (threat distribution, severity pie chart)
- [ ] Evidence display for each finding
- [ ] Brief generation and download

**4.3 Improve Visualizations**
- [ ] Add threat trend chart (timeline)
- [ ] Create confidence distribution visualization
- [ ] Add platform breakdown chart
- [ ] Implement findings table with sorting

### Deliverables
- [ ] Working dashboard at localhost:8501
- [ ] All core features functional
- [ ] Sample data displays correctly

### Time Estimate: 2-3 hours

---

## Day 5: Human Validation & Ground Truth

### Objectives
- Build validation dataset
- Manually review findings
- Document methodology

### Tasks

**5.1 Manual Review Process**
- [ ] Select 20-30 high-confidence findings
- [ ] Manually verify each one
- [ ] Document true positives vs false positives
- [ ] Identify classification errors

**5.2 Refine Classifier**
Based on manual review:
- [ ] Update threat prompts for better precision
- [ ] Adjust confidence thresholds
- [ ] Re-run classification on sample posts
- [ ] Measure improvement

**5.3 Document Methodology**
- [ ] Write validation approach in README
- [ ] Document confidence scoring rationale
- [ ] Create examples of each threat category

### Deliverables
- [ ] 20+ manual validations completed
- [ ] Accuracy metrics documented
- [ ] Refined classifier prompts

### Time Estimate: 3-4 hours

---

## Day 6: Research Brief & Final Report

### Objectives
- ✅ Report generation skeleton (DONE)
- Generate comprehensive intelligence brief
- Document limitations and methodology

### Tasks

**6.1 Generate Final Report**
```bash
# Run full pipeline with report generation
python agent.py
```

**6.2 Intelligence Brief Contents**
- [ ] Executive summary with key statistics
- [ ] Findings by threat category
- [ ] Severity and confidence distribution
- [ ] Methodology documentation
- [ ] Limitations and disclaimers
- [ ] Recommendations for further research

**6.3 Validation & Quality**
- [ ] Review brief for accuracy
- [ ] Verify all evidence is linked
- [ ] Check for clarity and professionalism
- [ ] Ensure methodology is reproducible

### Deliverables
- [ ] `threat_report.md` generated and reviewed
- [ ] 2-page executive summary created
- [ ] All findings properly cited

### Time Estimate: 2-3 hours

---

## Day 7: GitHub Publication & Presentation

### Objectives
- Publish GitHub repository
- Create presentation materials
- Finalize for 10a Labs submission

### Tasks

**7.1 Git Repository Setup**
```bash
cd threatscope-ai
git init
git add .
git commit -m "ThreatScope AI: Initial commit"
git remote add origin [your-github-repo]
git push -u origin main
```

**7.2 Documentation Verification**
- [ ] README.md complete and accurate
- [ ] QUICKSTART.md working end-to-end
- [ ] Code comments clear
- [ ] Requirements.txt complete

**7.3 Create Submission Package**
- [ ] GitHub repo with full source code
- [ ] Generated threat_report.md
- [ ] Dashboard screenshot (optional)
- [ ] Example output data

**7.4 Prepare for Interview**
- [ ] Be able to run live demo
- [ ] Explain threat classification framework
- [ ] Discuss limitations and safety
- [ ] Describe potential extensions

### Deliverables
- [ ] Public GitHub repository
- [ ] Complete documentation
- [ ] Runnable demo
- [ ] Application materials ready

### Time Estimate: 2-3 hours

---

## Checkpoint Checklist

### After Day 1
- [ ] APIs configured and tested
- [ ] Database initialized with sample data
- [ ] 100+ posts collected

### After Day 2
- [ ] Classifier working on sample posts
- [ ] 50+ posts classified
- [ ] Classifications reviewed for quality

### After Day 3
- [ ] High-confidence findings identified
- [ ] Signals extracted and stored
- [ ] Statistics dashboard working

### After Day 4
- [ ] Dashboard fully functional
- [ ] All visualizations working
- [ ] Brief generator operational

### After Day 5
- [ ] Manual validation completed on 20+ findings
- [ ] Classifier refined based on feedback
- [ ] Methodology documented

### After Day 6
- [ ] Final report generated
- [ ] Intelligence brief comprehensive
- [ ] All evidence linked and verified

### After Day 7
- [ ] GitHub repository public
- [ ] Documentation complete
- [ ] Ready for 10a Labs submission

---

## Success Criteria

By the end of 7 days, you will have:

✅ **Working System**
- Operational data collection pipeline
- LLM-powered threat classifier
- SQLite database with 500+ posts and classifications
- Interactive Streamlit dashboard
- Generated intelligence report

✅ **Research Methodology**
- FIST + MITRE F3 threat framework implemented
- Confidence and severity scoring system
- Human-in-the-loop validation workflow
- Evidence-linked reasoning

✅ **Professional Presentation**
- GitHub repository with clean code
- Comprehensive documentation
- Runnable quick-start guide
- Sample intelligence brief

✅ **Application Materials**
- Portfolio project demonstrating:
  - Research rigor
  - Technical implementation
  - Operational security
  - Ethical AI deployment

---

## Estimated Time Investment

| Day | Task | Hours |
|-----|------|-------|
| 1 | Setup & Collection | 1-2 |
| 2 | Classification | 2-3 |
| 3 | Database & Validation | 2 |
| 4 | Dashboard | 2-3 |
| 5 | Manual Review | 3-4 |
| 6 | Report Generation | 2-3 |
| 7 | GitHub & Submission | 2-3 |
| **TOTAL** | | **14-21 hours** |

**Practical Schedule**: 2-3 hours per day = 7 days
**Or: Intensive Mode**: 4-5 hours per day = 4-5 days

---

## Customization Options

### If Running Short on Time
- Skip Bluesky integration (Day 1)
- Use RSS feeds only, skip Reddit (Day 1)
- Sample 30 posts instead of 100+ (Days 2-3)
- Focus dashboard on overview, not detailed filters (Day 4)
- Skip automated validation, use manual review only (Day 5)

### If You Want to Go Deeper
- Add deepfake detection with computer vision (Day 6+)
- Implement voice cloning detection (Day 6+)
- Build cross-platform graph analysis (Day 6+)
- Add threat actor attribution (Day 6+)
- Set up automated monitoring with webhooks (Day 7+)

### For Advanced Features
See ROADMAP.md (to be created) for future enhancements

---

## Next Steps

1. **Configure APIs** (15 min)
   ```bash
   cp .env.example .env
   # Edit with your API keys
   ```

2. **Install dependencies** (5 min)
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run Day 1 tasks** (1-2 hours)
   ```bash
   python agent.py
   streamlit run dashboard.py
   ```

4. **Track progress** with this checklist

---

## Support & Troubleshooting

- **API Issues**: See README.md troubleshooting section
- **Code Errors**: Run with verbose logging: `python agent.py 2>&1 | tee agent.log`
- **Database Issues**: Reset with `rm threatscope.db && python -c "from database import init_db; init_db()"`

---

**Ready to start? Begin with Day 1 tasks above!**

Questions? Check README.md or QUICKSTART.md
