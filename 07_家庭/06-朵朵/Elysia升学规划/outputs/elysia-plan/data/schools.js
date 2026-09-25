// 院校与专业数据库 - Elysia 2026 A-Level 申请攻略
const schoolsData = {
  uk: {
    region: '英国 G5',
    flag: '🇬🇧',
    deadline_note: '牛剑UCAS截止: 2026年10月15日 | 其他G5: 2027年1月15日',
    schools: [
      {
        id: 'cambridge',
        name: '剑桥大学',
        nameEn: 'University of Cambridge',
        qsRank: '#5',
        emoji: '🏛️',
        city: 'Cambridge',
        matchScore: 4,
        programs: [
          {
            id: 'cam-math',
            name: 'Mathematics',
            nameCn: '数学',
            tags: ['math'],
            level: 'A*A*A - A*A*A*',
            subjects: '必须: Math + Further Math',
            test: 'TMUA (11月) + STEP (6月)',
            ielts: '7.5 (单项≥7.0)',
            deadline: '2026-10-15',
            url: 'https://www.undergraduate.study.cam.ac.uk/courses/mathematics',
            match: 5,
            comment: 'Elysia数学强项+AMC奖牌高度匹配，STEP需额外准备'
          },
          {
            id: 'cam-ns',
            name: 'Natural Sciences (Physical)',
            nameCn: '自然科学(物理方向，含化学)',
            tags: ['chemistry', 'math'],
            level: 'A*A*A',
            subjects: '必须: Math + 两门理科(含Chemistry)',
            test: 'NSAA (11月)',
            ielts: '7.5 (单项≥7.0)',
            deadline: '2026-10-15',
            url: 'https://www.undergraduate.study.cam.ac.uk/courses/natural-sciences',
            match: 3,
            comment: '可兼顾数学和化学，但需通过NSAA'
          }
        ]
      },
      {
        id: 'oxford',
        name: '牛津大学',
        nameEn: 'University of Oxford',
        qsRank: '#3',
        emoji: '🎓',
        city: 'Oxford',
        matchScore: 4,
        programs: [
          {
            id: 'ox-math',
            name: 'Mathematics',
            nameCn: '数学',
            tags: ['math'],
            level: 'A*A*A',
            subjects: '必须: Math + Further Math',
            test: 'MAT (11月，68分满分)',
            ielts: '7.5 (单项≥7.0)',
            deadline: '2026-10-15',
            url: 'https://www.ox.ac.uk/admissions/undergraduate/courses-listing/mathematics',
            match: 5,
            comment: 'AMC奖牌证明数学思维强，MAT需针对性训练'
          },
          {
            id: 'ox-stats',
            name: 'Mathematics and Statistics',
            nameCn: '数学与统计',
            tags: ['math', 'datascience'],
            level: 'A*A*A',
            subjects: '必须: Math',
            test: 'MAT (11月)',
            ielts: '7.5 (单项≥7.0)',
            deadline: '2026-10-15',
            url: 'https://www.ox.ac.uk/admissions/undergraduate/courses-listing/mathematics-and-statistics',
            match: 5,
            comment: '数学+数据科学完美交叉，强烈推荐'
          },
          {
            id: 'ox-chem',
            name: 'Chemistry',
            nameCn: '化学',
            tags: ['chemistry'],
            level: 'A*A*A',
            subjects: '必须: Math + Chemistry',
            test: 'Chemistry Admissions Test',
            ielts: '7.5 (单项≥7.0)',
            deadline: '2026-10-15',
            url: 'https://www.ox.ac.uk/admissions/undergraduate/courses-listing/chemistry',
            match: 2,
            comment: '需A-Level Chemistry，且非Elysia核心方向'
          }
        ]
      },
      {
        id: 'imperial',
        name: '帝国理工学院',
        nameEn: 'Imperial College London',
        qsRank: '#2',
        emoji: '🔬',
        city: 'London',
        matchScore: 5,
        programs: [
          {
            id: 'imp-math',
            name: 'Mathematics',
            nameCn: '数学',
            tags: ['math'],
            level: 'A*A*A* - A*A*A',
            subjects: '必须: Math + Further Math',
            test: 'TMUA (11月)',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.imperial.ac.uk/study/courses/mathematics/',
            match: 5,
            comment: 'QS全球#2理工校，数学系极强，TMUA比STEP更易准备'
          },
          {
            id: 'imp-ds',
            name: 'Economics, Finance and Data Science',
            nameCn: '经济、金融与数据科学',
            tags: ['datascience', 'math'],
            level: 'A*A*A',
            subjects: '必须: Math',
            test: 'TMUA ( mandatory )',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.imperial.ac.uk/study/courses/economics-finance-data-science/',
            match: 4,
            comment: '数据科学方向+商科思维，与Elysia模拟交易经历契合'
          },
          {
            id: 'imp-computing',
            name: 'Computing (with Data Science pathway)',
            nameCn: '计算(数据科学方向)',
            tags: ['datascience', 'math'],
            level: 'A*A*A* - A*A*A',
            subjects: '必须: Math + Further Math',
            test: 'TMUA',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.imperial.ac.uk/study/courses/computing/',
            match: 4,
            comment: 'CS+数据科学，就业面极广'
          }
        ]
      },
      {
        id: 'ucl',
        name: '伦敦大学学院',
        nameEn: 'University College London',
        qsRank: '#9',
        emoji: '🌐',
        city: 'London',
        matchScore: 4,
        programs: [
          {
            id: 'ucl-math',
            name: 'Mathematics',
            nameCn: '数学',
            tags: ['math'],
            level: 'A*A*A',
            subjects: '必须: Math + Further Math',
            test: 'STEP (建议)',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.ucl.ac.uk/prospective-students/undergraduate/degree-programmes/mathematics-bsc',
            match: 4,
            comment: '伦敦核心地段，数学系实力强'
          },
          {
            id: 'ucl-ds',
            name: 'Statistical Science',
            nameCn: '统计科学',
            tags: ['datascience', 'math'],
            level: 'A*A*A',
            subjects: '必须: Math',
            test: '无额外入学考',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.ucl.ac.uk/prospective-students/undergraduate/degree-programmes/statistical-science-bsc',
            match: 5,
            comment: '无额外入学考，数据科学核心专业，强烈推荐'
          },
          {
            id: 'ucl-arts',
            name: 'Arts and Sciences BASc',
            nameCn: '艺术与科学(跨学科)',
            tags: ['mathdesign', 'datascience'],
            level: 'ABB',
            subjects: '建议: Math',
            test: '无额外入学考',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.ucl.ac.uk/prospective-students/undergraduate/degree-programmes/arts-and-sciences-basc',
            match: 5,
            comment: '完美匹配数学+设计交叉! Elysia的美术功底+数学能力在此独特融合'
          }
        ]
      },
      {
        id: 'lse',
        name: '伦敦政治经济学院',
        nameEn: 'London School of Economics',
        qsRank: '#50',
        emoji: '📊',
        city: 'London',
        matchScore: 3,
        programs: [
          {
            id: 'lse-ds',
            name: 'Economics and Data Science',
            nameCn: '经济与数据科学',
            tags: ['datascience', 'math'],
            level: 'A*AA',
            subjects: '必须: Math',
            test: 'TMUA (强烈建议)',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.lse.ac.uk/study-at-lse/undergraduate/degrees/BSc-Economics-and-Data-Science',
            match: 4,
            comment: '2026新专业，数据科学+经济，LSE品牌加持'
          },
          {
            id: 'lse-stats',
            name: 'Data Science',
            nameCn: '数据科学',
            tags: ['datascience', 'math'],
            level: 'A*AA',
            subjects: '必须: Math',
            test: 'TMUA (强烈建议)',
            ielts: '7.0 (单项≥6.5)',
            deadline: '2027-01-15',
            url: 'https://www.lse.ac.uk/study-at-lse/undergraduate/degrees/BSc-Data-Science',
            match: 4,
            comment: '纯数据科学专业，LSE统计学系全球顶尖'
          }
        ]
      }
    ]
  },
  hk: {
    region: '中国香港',
    flag: '🇭🇰',
    deadline_note: '主轮截止: 2026年11月-2027年2月 | 港居民享本地学费(约HK$4.7万/年 vs 非本地HK$20万+/年)',
    schools: [
      {
        id: 'hku',
        name: '香港大学',
        nameEn: 'The University of Hong Kong',
        qsRank: '#17',
        emoji: '🏔️',
        city: 'Pokfulam',
        matchScore: 5,
        localFee: true,
        programs: [
          {
            id: 'hku-math',
            name: 'BSc Mathematics',
            nameCn: '数学学士',
            tags: ['math'],
            level: '2A*1A - 3A*',
            subjects: '必须: Math',
            test: '无额外入学考',
            ielts: '6.5 (单项≥6.0)',
            deadline: '2027-02',
            url: 'https://admissions.hku.hk/programme/bachelor-of-science-mathematics',
            match: 4,
            comment: '港大数学系，本地学费优势巨大'
          },
          {
            id: 'hku-ds',
            name: 'BSc Computer Science & Data Science',
            nameCn: '计算机科学与数据科学',
            tags: ['datascience', 'math'],
            level: '2A*1A - 3A*',
            subjects: '建议: Math + Physics/CS',
            test: '无额外入学考',
            ielts: '6.5 (单项≥6.0)',
            deadline: '2027-02',
            url: 'https://admissions.hku.hk/programme/bachelor-of-science-computer-science-and-data-science',
            match: 5,
            comment: 'CS+数据科学，港大王牌，本地生录取率远高于非本地'
          },
          {
            id: 'hku-design',
            name: 'BA Design+',
            nameCn: '设计+(跨学科)',
            tags: ['mathdesign'],
            level: '3A',
            subjects: '无硬性科目要求',
            test: '需提交作品集 + 面试',
            ielts: '6.5 (单项≥6.0)',
            deadline: '2027-01',
            url: 'https://design.hku.hk/programme/ba-design',
            match: 5,
            comment: '数学+设计完美交叉! Elysia美术功底+二次元审美是巨大优势，需准备作品集'
          }
        ]
      },
      {
        id: 'hkust',
        name: '香港科技大学',
        nameEn: 'The Hong Kong University of Science and Technology',
        qsRank: '#47',
        emoji: '🚀',
        city: 'Clear Water Bay',
        matchScore: 5,
        localFee: true,
        programs: [
          {
            id: 'hkust-math',
            name: 'BSc in Mathematics',
            nameCn: '数学学士',
            tags: ['math'],
            level: 'AAB - AAA',
            subjects: '必须: Math',
            test: '无额外入学考',
            ielts: '6.5 (单项≥6.0)',
            deadline: '2027-01',
            url: 'https://join.ust.hk/programs/bachelor-of-science-in-mathematics',
            match: 4,
            comment: '科大数学系研究实力强，本地学费'
          },
          {
            id: 'hkust-ds',
            name: 'BSc in Data Science and Technology',
            nameCn: '数据科学与科技',
            tags: ['datascience', 'math'],
            level: 'A*A*A - AAA',
            subjects: '必须: Math + 一门理科/CS',
            test: '无额外入学考',
            ielts: '6.5 (单项≥6.0)',
            deadline: '2027-01',
            url: 'https://join.ust.hk/programs/bachelor-of-science-in-data-science-and-technology',
            match: 5,
            comment: '数据科学核心专业，科大CS/DS排名亚洲顶尖'
          },
          {
            id: 'hkust-isd',
            name: 'BEng in Integrative Systems and Design',
            nameCn: '综合系统与设计',
            tags: ['mathdesign', 'datascience'],
            level: 'AAB - AAA',
            subjects: '建议: Math',
            test: '无额外入学考',
            ielts: '6.5 (单项≥6.0)',
            deadline: '2027-01',
            url: 'https://join.ust.hk/programs/bachelor-of-engineering-in-integrative-systems-and-design',
            match: 4,
            comment: '工程+设计思维+AI，跨学科项目，适合数学+设计兴趣'
          }
        ]
      },
      {
        id: 'cuhk',
        name: '香港中文大学',
        nameEn: 'The Chinese University of Hong Kong',
        qsRank: '#36',
        emoji: '🦅',
        city: 'Sha Tin',
        matchScore: 4,
        localFee: true,
        programs: [
          {
            id: 'cuhk-math',
            name: 'BSc in Mathematics',
            nameCn: '数学学士',
            tags: ['math'],
            level: 'AAA',
            subjects: '必须: Math',
            test: '无额外入学考',
            ielts: '6.0',
            deadline: '2027-01',
            url: 'https://www.math.cuhk.edu.hk/programmes/undergraduate/major/math/',
            match: 4,
            comment: '中大数学系传统强校，沙田校园优美'
          },
          {
            id: 'cuhk-ds',
            name: 'BSc in Data Science and Analytics',
            nameCn: '数据科学与分析',
            tags: ['datascience', 'math'],
            level: 'AAA - AAB',
            subjects: '必须: Math',
            test: '无额外入学考',
            ielts: '6.0',
            deadline: '2027-01',
            url: 'https://www.dsaa.cuhk.edu.hk/',
            match: 5,
            comment: '数据科学专业，IELTS要求仅6.0，对Elysia友好'
          }
        ]
      },
      {
        id: 'cityu',
        name: '香港城市大学',
        nameEn: 'City University of Hong Kong',
        qsRank: '#62',
        emoji: '🏙️',
        city: 'Kowloon Tong',
        matchScore: 3,
        localFee: true,
        programs: [
          {
            id: 'cityu-ds',
            name: 'BSc in Data Science',
            nameCn: '数据科学',
            tags: ['datascience', 'math'],
            level: 'ABB - AAA',
            subjects: '建议: Math',
            test: '无额外入学考',
            ielts: '6.5',
            deadline: '2027-02',
            url: 'https://www.cityu.edu.hk/ds/',
            match: 4,
            comment: '保底选择，数据科学专业扎实，九龙塘市中心'
          },
          {
            id: 'cityu-creative',
            name: 'BA in Creative Media',
            nameCn: '创意媒体',
            tags: ['mathdesign'],
            level: 'ABB',
            subjects: '无硬性要求',
            test: '需提交作品集',
            ielts: '6.5',
            deadline: '2027-02',
            url: 'https://www.cityu.edu.hk/sccm/',
            match: 3,
            comment: '创意媒体+数字艺术，可作为设计方向保底'
          }
        ]
      },
      {
        id: 'polyu',
        name: '香港理工大学',
        nameEn: 'The Hong Kong Polytechnic University',
        qsRank: '#57',
        emoji: '🎨',
        city: 'Hung Hom',
        matchScore: 3,
        localFee: true,
        programs: [
          {
            id: 'polyu-ds',
            name: 'BSc in Data Science and Analytics',
            nameCn: '数据科学与分析',
            tags: ['datascience', 'math'],
            level: 'BBB - AAB',
            subjects: '建议: Math',
            test: '无额外入学考',
            ielts: '6.0',
            deadline: '2027-02',
            url: 'https://www.polyu.edu.hk/dsaa/',
            match: 3,
            comment: '保底选择，入学门槛较友好'
          },
          {
            id: 'polyu-design',
            name: 'BA in Design (Environmental/Visual Comm)',
            nameCn: '设计学士(环境/视觉传达)',
            tags: ['mathdesign'],
            level: 'BBB',
            subjects: '无硬性要求',
            test: '需提交作品集 + 面试',
            ielts: '6.0',
            deadline: '2027-02',
            url: 'https://www.polyu.edu.hk/sd/',
            match: 4,
            comment: '理大设计学院亚洲顶尖! Elysia美术功底极具竞争力'
          }
        ]
      }
    ]
  },
  japan: {
    region: '日本',
    flag: '🇯🇵',
    deadline_note: '多数需先考EJU(日本留学考试) | 英语项目可直接申请 | 日语项目需N1-N2',
    schools: [
      {
        id: 'utokyo',
        name: '东京大学',
        nameEn: 'The University of Tokyo',
        qsRank: '#28',
        emoji: '🗼',
        city: 'Tokyo',
        matchScore: 3,
        programs: [
          {
            id: 'utokyo-science',
            name: 'Faculty of Science - Mathematics',
            nameCn: '理学部 数学科',
            tags: ['math'],
            level: 'A-Level A*AA + EJU高分',
            subjects: 'EJU: 数学Course2 + 理科2科目',
            test: 'EJU + 东大二次试验',
            ielts: '日语N1或TOEFL 80+(英语项目)',
            deadline: 'EJU: 6月/11月 | 出愿: 12月-1月',
            url: 'https://www.u-tokyo.ac.jp/en/prospective-students/undergraduate.html',
            match: 2,
            comment: '日本最高学府，需日语N1+东大二次试验，难度极高'
          },
          {
            id: 'utokyo-peac',
            name: 'Program on Environment and Society (PEAK)',
            nameCn: 'PEAK英语国际项目',
            tags: ['datascience'],
            level: 'A-Level AAA + 面试',
            subjects: '无硬性科目',
            test: '面试 + 文书',
            ielts: 'TOEFL 80+ / IELTS 6.5+',
            deadline: '2026-12',
            url: 'https://www.c.u-tokyo.ac.jp/en/peak/',
            match: 3,
            comment: '英语授课，但偏环境/社会方向，非核心匹配'
          }
        ]
      },
      {
        id: 'kyoto',
        name: '京都大学',
        nameEn: 'Kyoto University',
        qsRank: '#46',
        emoji: '⛩️',
        city: 'Kyoto',
        matchScore: 3,
        programs: [
          {
            id: 'kyoto-science',
            name: 'Faculty of Science - Mathematics',
            nameCn: '理学部 数学科',
            tags: ['math'],
            level: 'A-Level A*AA + EJU高分',
            subjects: 'EJU: 数学Course2 + 理科',
            test: 'EJU + 京大二次试验',
            ielts: '日语N1或TOEFL 85+(英语项目)',
            deadline: 'EJU: 6月/11月 | 出愿: 12月-1月',
            url: 'https://www.kyoto-u.ac.jp/en/education-campus/international-undergraduate',
            match: 2,
            comment: '京大数学自由度高，但需日语+二次试验'
          },
          {
            id: 'kyoto-iup',
            name: 'iUP International Undergraduate Program',
            nameCn: '国际本科项目(英语)',
            tags: ['math', 'datascience'],
            level: 'A-Level AAA + 面试',
            subjects: '无硬性科目',
            test: '面试 + 文书',
            ielts: 'TOEFL 80+ / IELTS 6.5+',
            deadline: '2026-12',
            url: 'https://www.kyoto-u.ac.jp/en/education-campus/iup',
            match: 3,
            comment: '英语授课国际项目，含日语培训'
          }
        ]
      },
      {
        id: 'tsukuba',
        name: '筑波大学',
        nameEn: 'University of Tsukuba',
        qsRank: '#201-210',
        emoji: '🌸',
        city: 'Tsukuba',
        matchScore: 3,
        programs: [
          {
            id: 'tsukuba-gs',
            name: 'Global Science Course (College of Biological Sciences)',
            nameCn: '全球科学课程',
            tags: ['datascience', 'math'],
            level: 'A-Level AAB + 面试',
            subjects: '建议: Math + Science',
            test: '面试 + 文书',
            ielts: 'TOEFL 80+ / IELTS 6.0+',
            deadline: '2026-12',
            url: 'https://www.tsukuba.ac.jp/en/education/global-science-course/',
            match: 3,
            comment: '英语授课，筑波科学城环境好，但排名较低'
          },
          {
            id: 'tsukuba-it',
            name: 'College of Information Science',
            nameCn: '情报学群(计算机科学)',
            tags: ['datascience', 'math'],
            level: 'A-Level AAB + EJU',
            subjects: 'EJU: 数学Course2',
            test: 'EJU + 校内考',
            ielts: '日语N2或英语TOEFL 80+',
            deadline: 'EJU: 6月/11月',
            url: 'https://www.tsukuba.ac.jp/en/education/college-of-information-science/',
            match: 3,
            comment: 'CS/数据科学方向，可英语或日语申请'
          }
        ]
      },
      {
        id: 'waseda',
        name: '早稻田大学',
        nameEn: 'Waseda University',
        qsRank: '#193',
        emoji: '🎌',
        city: 'Tokyo (Shinjuku)',
        matchScore: 4,
        programs: [
          {
            id: 'waseda-sils',
            name: 'School of International Liberal Studies (SILS)',
            nameCn: '国际教养学部',
            tags: ['datascience', 'mathdesign'],
            level: 'A-Level AAB + 面试',
            subjects: '无硬性科目',
            test: '面试 + 文书 + 英语面试',
            ielts: 'TOEFL 85+ / IELTS 6.5+',
            deadline: '2026-09 (AO入试)',
            url: 'https://www.waseda.jp/fp/sils/en/',
            match: 4,
            comment: '英语授课，可修数据科学+媒体研究，新宿校区便利'
          },
          {
            id: 'waseda-ese',
            name: 'School of Fundamental Science and Engineering - Information Science',
            nameCn: '基干理工学部 情报理工学科',
            tags: ['datascience', 'math'],
            level: 'A-Level AAA + EJU',
            subjects: 'EJU: 数学Course2 + 物理',
            test: 'EJU + 校内考',
            ielts: '日语N2或TOEFL 80+',
            deadline: 'EJU: 6月/11月',
            url: 'https://www.waseda.jp/fst/en/',
            match: 3,
            comment: '理工科核心，需日语或EJU'
          }
        ]
      }
    ]
  }
}

// 行动时间线
const actionTimeline = [
  {
    month: '2026年8月',
    title: '启动准备',
    emoji: '🚀',
    tasks: [
      { text: '确定A-Level选课: Math, Further Math, + 1-2门(建议Physics/CS/Chemistry)', done: false },
      { text: '雅思目标: 从5.5提升到6.5+(港校)/7.0+(英校)', done: false },
      { text: '开始TMUA/MAT备考(牛剑/帝国/LSE必须)', done: false },
      { text: '注册UCAS账号，了解申请流程', done: false }
    ]
  },
  {
    month: '2026年9月',
    title: '正式开学',
    emoji: '📚',
    tasks: [
      { text: '香港蔚来学校11年级开学，全力A-Level课程', done: false },
      { text: '每周TMUA/MAT真题练习(至少3套/月)', done: false },
      { text: '开始准备作品集(如目标Design+/设计类专业)', done: false },
      { text: '参加AMC/BMO等数学竞赛，积累奖牌', done: false }
    ]
  },
  {
    month: '2026年10月',
    title: '牛剑冲刺',
    emoji: '🎯',
    tasks: [
      { text: '10月15日前: 提交牛剑UCAS申请(如目标Cambridge/Oxford)', done: false },
      { text: '10月底: 参加TMUA考试(帝国/LSE也需要)', done: false },
      { text: '11月初: 参加MAT考试(牛剑数学必须)', done: false },
      { text: '准备牛剑面试(12月初)', done: false }
    ]
  },
  {
    month: '2026年11月',
    title: '考试月',
    emoji: '📝',
    tasks: [
      { text: '11月: TMUA考试(如10月未考)', done: false },
      { text: '11月: MAT考试(如10月未考)', done: false },
      { text: '11月: EJU考试(如目标日本)', done: false },
      { text: '提交港校申请(HKU/HKUST/CUHK主轮)', done: false }
    ]
  },
  {
    month: '2026年12月',
    title: '面试与文书',
    emoji: '🎤',
    tasks: [
      { text: '12月初: 牛剑面试', done: false },
      { text: '完成所有港校申请文书', done: false },
      { text: '提交日本大学英语项目申请', done: false },
      { text: '作品集定稿(如申请设计类)', done: false }
    ]
  },
  {
    month: '2027年1月',
    title: '全面申请',
    emoji: '📮',
    tasks: [
      { text: '1月15日前: 提交帝国/UCL/LSE UCAS申请', done: false },
      { text: '提交CityU/PolyU申请', done: false },
      { text: '准备AS/A-Level模拟考试', done: false }
    ]
  },
  {
    month: '2027年2-3月',
    title: '等待与补充',
    emoji: '⏳',
    tasks: [
      { text: '等待港校offer', done: false },
      { text: '补充UCAS申请(如有剩余名额)', done: false },
      { text: '继续雅思刷分(如未达标)', done: false }
    ]
  },
  {
    month: '2027年4月',
    title: '关键节点',
    emoji: '⚠️',
    tasks: [
      { text: '优才计划续签(确保香港居民身份有效)', done: false },
      { text: '确认港校本地生学费资格', done: false },
      { text: 'A-Level AS考试(如学校安排)', done: false }
    ]
  },
  {
    month: '2027年5-6月',
    title: '最终冲刺',
    emoji: '🏆',
    tasks: [
      { text: 'A-Level A2最终考试', done: false },
      { text: '6月: STEP考试(如目标Cambridge/UCL数学)', done: false },
      { text: '收到offer，做出最终选择', done: false }
    ]
  }
]

// 结论与建议
const conclusions = {
  summary: 'Elysia的核心竞争力是"数学+设计"的稀缺交叉能力。AMC奖牌证明数学实力，美术功底和二次元文化敏感度是独特差异化优势。建议以数据科学/数学为主线，以数学+设计交叉为特色，构建"理性思维+创意表达"的申请叙事。',
  topPicks: [
    {
      school: 'UCL Arts & Sciences BASc',
      reason: '完美匹配数学+设计交叉，A-level要求ABB(可达)，无额外入学考',
      priority: '冲刺',
      color: '#e74c3c'
    },
    {
      school: 'HKU BSc CS & Data Science',
      reason: '港校本地学费(省80%)，数据科学王牌，IELTS仅6.5',
      priority: '主攻',
      color: '#f39c12'
    },
    {
      school: 'HKUST BSc Data Science & Technology',
      reason: '亚洲DS顶尖，本地学费，与模拟交易经历契合',
      priority: '主攻',
      color: '#f39c12'
    },
    {
      school: 'Imperial Mathematics',
      reason: 'QS全球#2理工，TMUA比STEP更易准备',
      priority: '冲刺',
      color: '#e74c3c'
    },
    {
      school: 'Oxford Mathematics & Statistics',
      reason: '数学+统计完美交叉，MAT考试适合数学强项',
      priority: '冲刺',
      color: '#e74c3c'
    },
    {
      school: 'CUHK BSc Data Science & Analytics',
      reason: 'IELTS仅6.0(对Elysia友好)，数据科学核心专业',
      priority: '稳妥',
      color: '#27ae60'
    }
  ],
  keyActions: [
    '雅思从5.5提升到6.5+(10月前)→ 决定能否申请港校/英校',
    'TMUA/MAT备考(9月开始)→ 决定能否冲刺牛剑/帝国',
    '作品集启动(9月开始)→ 决定能否申请Design+/创意媒体',
    '优才续签(2027年4月)→ 决定能否享受港校本地学费(省80%)',
    'A-Level选课确认: Math + Further Math + 1-2门 → 决定申请范围'
  ],
  strategyNote: '建议采用"3+2+1"策略: 3所港校(本地学费优势) + 2所英国G5(冲刺) + 1所日本英语项目(备选)。港校是性价比最高的选择，本地学费每年仅HK$4.7万 vs 非本地HK$20万+，四年节省超60万港币。'
}

module.exports = {
  schoolsData,
  actionTimeline,
  conclusions
}
