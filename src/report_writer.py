# src/report_writer.py
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os


class DocxGenerator:
    def __init__(self):
        self.doc = Document()
        self._setup_styles()

    def _setup_styles(self):
        """문서의 기본 폰트나 스타일 설정 (선택사항)"""
        style = self.doc.styles['Normal']
        font = style.font
        font.name = 'Malgun Gothic'  # 한글 폰트 설정 (시스템에 있어야 함)
        font.size = Pt(10)

    def create_report(self, url, screenshot_path, page_data, api_logs, interactive_elements=None, whois_data=None):
        """
        모든 데이터를 받아서 순서대로 문서에 작성합니다.
        """
        # 1. 제목 및 기본 정보
        self.doc.add_heading(f'웹사이트 분석 보고서', 0)

        p = self.doc.add_paragraph()
        p.add_run(f"분석 대상 URL: ").bold = True
        p.add_run(url + "\n")
        p.add_run(f"사이트 제목: ").bold = True
        p.add_run(page_data.get('title', 'N/A'))

        # 2. 초기 화면 스크린샷
        self.doc.add_heading('1. 초기 화면 (Screen Capture)', level=1)
        if os.path.exists(screenshot_path):
            try:
                # 페이지 폭에 맞춰 이미지 삽입 (약 6인치)
                self.doc.add_picture(screenshot_path, width=Inches(6.0))
            except Exception as e:
                self.doc.add_paragraph(f"[이미지 삽입 실패: {e}]")
        else:
            self.doc.add_paragraph("[스크린샷 파일을 찾을 수 없음]")

        # 3. 기능 및 구조 분석
        self.doc.add_heading('2. 기능 및 구조 분석', level=1)

        # 3-1. 주요 기능 추정
        self.doc.add_heading('2-1. 주요 기능 (추정)', level=2)
        features = page_data.get('guessed_features', [])
        if features:
            for feat in features:
                self.doc.add_paragraph(feat, style='List Bullet')
        else:
            self.doc.add_paragraph("특이 기능 발견되지 않음.")

        # 3-2. 구성 요소 요약
        self.doc.add_heading('2-2. 구성 요소 요약', level=2)
        links = page_data.get('links', {})
        buttons = page_data.get('buttons', {})

        table = self.doc.add_table(rows=1, cols=2)
        table.style = 'Table Grid'
        hdr_cells = table.rows[0].cells
        hdr_cells[0].text = '항목'
        hdr_cells[1].text = '분석 결과'

        row_data = [
            ("Meta 설명", page_data.get('meta_description', '-')),
            ("총 링크 수", f"{links.get('total', 0)}개 (내부: {links.get('internal', 0)}, 외부: {links.get('external', 0)})"),
            ("버튼 수", f"{buttons.get('total', 0)}개 (Submit: {buttons.get('submit_type', 0)})"),
            ("입력 필드 수", f"{len(page_data.get('inputs', []))}개")
        ]

        for item, value in row_data:
            row_cells = table.add_row().cells
            row_cells[0].text = item
            row_cells[1].text = str(value)

        # 4. API 통신 분석
        self.doc.add_heading('3. API 통신 분석 (Network Logs)', level=1)
        self.doc.add_paragraph(f"수집된 주요 API 요청 수: {len(api_logs)}건")

        if api_logs:
            # 테이블 생성 (번호, Method, URL, IP, 상태)
            api_table = self.doc.add_table(rows=1, cols=4)
            api_table.style = 'Table Grid'
            api_table.autofit = False

            headers = api_table.rows[0].cells
            headers[0].text = 'Method'
            headers[1].text = 'URL (Path)'
            headers[2].text = 'Server IP'
            headers[3].text = 'Status'

            # 너무 많으면 상위 20개만 기록
            for log in api_logs[:20]:
                row_cells = api_table.add_row().cells
                row_cells[0].text = log['method']
                # URL이 너무 길면 잘라서 보여줌
                row_cells[1].text = (log['url'][:40] + '...') if len(log['url']) > 40 else log['url']
                row_cells[2].text = f"{log['domain']}\n({log['ip']})"
                row_cells[3].text = str(log['status'])
        else:
            self.doc.add_paragraph("감지된 XHR/Fetch 요청이 없습니다.")

        self.doc.add_page_break()
        self.doc.add_heading('4. 서버 IP WHOIS 정보', level=1)
        self.doc.add_paragraph("분석 과정에서 식별한 서버 IP의 소유자 정보 분석")

        if whois_data:
            #테이블 구조 : IP - 국가 - ISP - 할당 대역
            table = self   .doc.add_table(rows=1, cols=4)
            table.style = 'Table Grid'

            hdr = table.rows[0].cells
            hdr[0].text = 'IP Address'
            hdr[1].text = '국가'
            hdr[2].text = '소유 기관'
            hdr[3].text = 'IP 대역'

            for cell in hdr :
                cell.width = Inches(1.5)

            for info in whois_data:
                row_cells = table.add_row().cells
                row_cells[0].text = info['ip']
                row_cells[1].text = info['country']
                row_cells[2].text = info['org']
                row_cells[3].text = info['cidr']

            else :
                self.doc.add_paragraph("조회된 WHOIS 정보 없음.")


        self.doc.add_page_break()  # 새 페이지에서 시작
        self.doc.add_heading('5. 상호작용 요소 상세 분석', level=1)
        self.doc.add_paragraph("사용자가 클릭 가능한 주요 요소들의 시각적 형태와 연결 동작을 분석합니다.")

        if interactive_elements:
            # 테이블 생성: [이미지] | [텍스트/유형] | [실행 동작]
            table = self.doc.add_table(rows=1, cols=3)
            table.style = 'Table Grid'

            hdr_cells = table.rows[0].cells
            hdr_cells[0].text = '요소 이미지'
            hdr_cells[1].text = '식별 정보'
            hdr_cells[2].text = '실행 동작 (Action)'

            # 열 너비 조정 (대략적으로)
            for cell in table.rows[0].cells:
                cell.width = Inches(2.0)

            for item in interactive_elements:
                row_cells = table.add_row().cells

                # 1열: 이미지 삽입
                p = row_cells[0].paragraphs[0]
                if os.path.exists(item['image_path']):
                    try:
                        run = p.add_run()
                        run.add_picture(item['image_path'], width=Inches(1.5))  # 너비 고정
                    except:
                        p.text = "[이미지 오류]"

                # 2열: 텍스트 및 태그 유형
                row_cells[1].text = f"Text: {item['text']}\nTag: <{item['type']}>"

                # 3열: 동작 정보 (URL 등)
                row_cells[2].text = item['action']

        else:
            self.doc.add_paragraph("분석 가능한 상호작용 요소를 찾지 못했습니다.")

    def save_file(self, filename):
        try:
            self.doc.save(filename)
            print(f"[Report] Document saved successfully: {filename}")
        except Exception as e:
            print(f"[Report] Error saving document: {e}")