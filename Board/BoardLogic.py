import numpy as np

from Board.BoardMoveDetails import BoardTurnDetails
from GameSettings.DefaultSettings import *
import copy
import random

class BasicBoardLogic:
    def __init__(self, board_row=3, board_col=3, number_score_to_win=3):
        self._number_of_turn = 0
        self.board_row = board_row
        self.board_col = board_col
        self.number_score_to_win = number_score_to_win
        self.square_size = board_width // self.board_row
        self._squares = np.zeros((board_row, board_col))
        self._listMarked = []
        self._winningLine = None

    # Đánh dấu ô 
    def markSquare(self, playerId, row, col):
        self._squares[row][col] = playerId
        self._number_of_turn += 1
        self._listMarked.append(BoardTurnDetails(playerId, row, col))

    # Nhận trạng thái chiến thắng
    def getWinningState(self):
        if len(self._listMarked) == 0:
            return 0
        lastTurn = self._listMarked[-1]
        playerId = lastTurn.playerId
        row, col = lastTurn.position
        if self.checkLineFromPos(playerId, row, col, 1, 0)[0] \
                or self.checkLineFromPos(playerId, row, col, 0, 1)[0] \
                or self.checkLineFromPos(playerId, row, col, 1, 1)[0] \
                or self.checkLineFromPos(playerId, row, col, 1, -1)[0]:
            return playerId
        return 0

    def checkLineFromPos(self, playerId, row, col, changeRow, changeCol):
        # Nhận giá trị vị trí ô phía trước
        tempRow = row - changeRow
        tempCol = col - changeCol
        count = 1
        startPoint = (row, col)
        while self.isValidateRowCol(tempRow, tempCol) and self._squares[tempRow][tempCol] == playerId:
            count += 1
            startPoint = (tempRow, tempCol)
            tempRow -= changeRow
            tempCol -= changeCol

        # Nhận giá trị vị trí ô phía sau
        tempRow = row + changeRow
        tempCol = col + changeCol
        endPoint = (row, col)
        while self.isValidateRowCol(tempRow, tempCol) and self._squares[tempRow][tempCol] == playerId:
            count += 1
            endPoint = (tempRow, tempCol)
            tempRow += changeRow
            tempCol += changeCol

        # Nếu thắng thì lưu điểm bắt đầu và kết thúc
        isWinning = count >= self.number_score_to_win
        if isWinning:
            self._winningLine = (startPoint, endPoint)
        return isWinning, count


    def getEmptySquares(self):
        emptySqrs = []
        [emptySqrs.append((row, col)) for row in range(self.board_row)
         for col in range(self.board_col) if self._squares[row][col] == 0]
        return emptySqrs

    def getNeighborEmptySquares(self, pos_x, pos_y):
        neightBorSqrs = []
        [neightBorSqrs.append((row, col)) for row in range(pos_x - 1, pos_x + 2) \
         for col in range(pos_y - 1, pos_y + 2) if self.isValidateRowCol(row, col)
         and self._squares[row][col] == 0]
        return neightBorSqrs

    def getScoreOfPosition(self, playerId, row, col):
        return max(self.checkLineFromPos(playerId, row, col, 1, 0)[1],
                   self.checkLineFromPos(playerId, row, col, 0, 1)[1],
                   self.checkLineFromPos(playerId, row, col, 1, 1)[1],
                   self.checkLineFromPos(playerId, row, col, 1, -1)[1])

    def isFull(self):
        return self._number_of_turn >= self.board_row * self.board_col

    def isEmpty(self):
        return self._number_of_turn == 0

    def isOver(self):
        return self.getWinningState() != 0 or self.isFull()

    def isSquareEmpty(self, row, col):
        if self.isValidateRowCol(row, col):
            return self._squares[row][col] == 0
        return False

    def copyBoard(self, other):
        self.board_col = other.board_col
        self.board_row = other.board_row
        self._number_of_turn = other.getNumberOfTurn()
        self._winningLine = copy.deepcopy(other.getWinningLine())
        self._listMarked = copy.deepcopy(other.getListMarked())
        self._squares = copy.deepcopy(other.getSquares())

    def getNumberOfTurn(self):
        return self._number_of_turn

    def getWinningLine(self):
        return self._winningLine

    def getListMarked(self):
        return self._listMarked

    def getSquares(self):
        return self._squares

    # Kiểm tra vị trí có hợp lệ hay không
    def isValidateRowCol(self, row_index, col_index):
        if 0 <= row_index < self.board_row and 0 <= col_index < self.board_col:
            return True
        return False

    def row_to_list(self,y,x,dy,dx,yf,xf):
        '''
        trả về list của y,x từ yf,xf
        
        '''
        row = []
        while y != yf + dy or x !=xf + dx:
            row.append(self._squares[y][x])
            y += dy
            x += dx
        return row

    def score_of_list(self,lis,col):
        
        blank = lis.count(0)
        filled = lis.count(col)
        
        if blank + filled < 5:
            return -1
        elif blank == 5:
            return 0
        else:
            return filled

    def score_of_row(self,cordi,dy,dx,cordf,col):
        '''
        trả về một list với mỗi phần tử đại diện cho số điểm của 5 khối

        '''
        colscores = []
        y,x = cordi
        yf,xf = cordf
        row = self.row_to_list(y,x,dy,dx,yf,xf)
        for start in range(len(row)-4):
            lis = row[start:start+5]
            score = self.score_of_list( lis  ,col )
            colscores.append(score)
        
        return colscores

    def score_ready(self,scorecol):
        '''
        Khởi tạo hệ thống điểm

        '''
        sumcol = {0: {},1: {},2: {},3: {},4: {},5: {},-1: {}}
        for key in scorecol:
            for score in scorecol[key]:
                if key in sumcol[score]:
                    sumcol[score][key] += 1
                else:
                    sumcol[score][key] = 1
                
        return sumcol

    def score_of_col_one(self,col,y,x):
        '''
        trả lại điểm số của column trong y,x theo 4 hướng,
        key: điểm số khối đơn vị đó -> chỉ ktra 5 khối thay vì toàn bộ
        '''
        
        scores = {(0,1):[],(-1,1):[],(1,0):[],(1,1):[]}
        
        scores[(0,1)].extend(self.score_of_row(self.march(y,x,0,-1,4), 0, 1,self.march(y,x,0,1,4), col))
        
        scores[(1,0)].extend(self.score_of_row(self.march(y,x,-1,0,4), 1, 0,self.march(y,x,1,0,4), col))
        
        scores[(1,1)].extend(self.score_of_row(self.march(y,x,-1,-1,4), 1, 1,self.march(y,x,1,1,4), col))

        scores[(-1,1)].extend(self.score_of_row(self.march(y,x,-1,1,4), 1,-1,self.march(y,x,1,-1,4), col))
        
        return self.score_ready(scores )

    def march(self,y,x,dy,dx,length):
        '''
        tìm vị trí xa nhất trong dy,dx trong khoảng length

        '''
        yf = y + length*dy 
        xf = x + length*dx
        # chừng nào yf,xf không có trong board
        while not self.isValidateRowCol(yf,xf):
            yf -= dy
            xf -= dx
            
        return yf,xf

    def possible_moves(self):  
        '''
        khởi tạo danh sách tọa độ có thể có tại danh giới các nơi đã đánh phạm vi 3 đơn vị
        '''
        #mảng taken lưu giá trị của người chơi và của máy trên bàn cờ
        taken = []
        # mảng directions lưu hướng đi (8 hướng)
        directions = [(0,1),(0,-1),(1,0),(-1,0),(1,1),(-1,-1),(-1,1),(1,-1)]
        # cord: lưu các vị trí không đi 
        cord = {}
        
        for i in range(self.board_row):
            for j in range(self.board_row):
                if self._squares[i][j] != 0:
                    taken.append((i,j))
        ''' duyệt trong hướng đi và mảng giá trị trên bàn cờ của người chơi và máy, kiểm tra nước không thể đi(trùng với 
        nước đã có trên bàn cờ)
        '''
        for direction in directions:
            dy,dx = direction
            for coord in taken:
                y,x = coord
                for length in [1,2,3,4]:
                    move = self.march(y,x,dy,dx,length)
                    if move not in taken and move not in cord:
                        cord[move]=False
        return cord

    def winning_situation(self,sumcol):
        '''
        trả lại tình huống chiến thắng dạng như:
        {0: {}, 1: {(0, 1): 4, (-1, 1): 3, (1, 0): 4, (1, 1): 4}, 2: {}, 3: {}, 4: {}, 5: {}, -1: {}}
        1-5 lưu điểm có độ nguy hiểm từ thấp đến cao,
        -1 là rơi vào trạng thái tồi, cần phòng thủ
        '''
        
        if 1 in sumcol[5].values():
            return 5
        elif len(sumcol[4])>=2 or (len(sumcol[4])>=1 and max(sumcol[4].values())>=2):
            return 4
        elif self.TF34score(sumcol[3],sumcol[4]):
            return 4
        else:
            score3 = sorted(sumcol[3].values(),reverse = True)
            if len(score3) >= 2 and score3[0] >= score3[1] >= 2:
                return 3
        return 0
    
    def TF34score(self,score3,score4):
        '''
        trả lại trường hợp chắc chắn có thể thắng(4 ô liên tiếp)
        '''
        for key4 in score4:
            if score4[key4] >=1:
                for key3 in score3:
                    if key3 != key4 and score3[key3] >=2:
                            return True
        return False
    def sum_sumcol_values(self,sumcol):
        '''
        hợp nhất điểm của mỗi hướng
        '''
        
        for key in sumcol:
            if key == 5:
                sumcol[5] = int(1 in sumcol[5].values())
            else:
                sumcol[key] = sum(sumcol[key].values())

class AdvancedBoardLogic(BasicBoardLogic):
    def getMostBenefitSqrs(self, selfPlayer, oppositePlayer):
        if self.isFull():
            return -1, -1
        emptySqr = self.getEmptySquares()
        max_point = 0
        next_mark = emptySqr[0]
        for row, col in emptySqr:
            self_point = self.getScoreOfPosition(selfPlayer, row, col)
            opposite_point = self.getScoreOfPosition(oppositePlayer, row, col)
            max_point = max(max_point, self_point, opposite_point)
            if opposite_point >= max_point:
                next_mark = (row, col)
            if self_point >= max_point:
                next_mark = (row, col)
        return next_mark
        
    def stupid_score(self,col,anticol,y,x):
        '''
        cố gắng di chuyển y,x
        trả về điểm số tượng trưng lợi thế 
        '''
        # global colors
        M = 1000
        res,adv, dis = 0, 0, 0
        
        #tấn công
        self._squares[y][x] = col
        #draw_stone(x,y,colors[col])
        sumcol = self.score_of_col_one(col,y,x)       
        a = self.winning_situation(sumcol)
        adv += a * M
        self.sum_sumcol_values(sumcol)
        #{0: 0, 1: 15, 2: 0, 3: 0, 4: 0, 5: 0, -1: 0}
        adv +=  sumcol[-1] + sumcol[1] + 4*sumcol[2] + 8*sumcol[3] + 16*sumcol[4]
        
        #phòng thủ
        self._squares[y][x]=anticol
        sumanticol = self.score_of_col_one(anticol,y,x)  
        d = self.winning_situation(sumanticol)
        dis += d * (M-100)
        self.sum_sumcol_values(sumanticol)
        dis += sumanticol[-1] + sumanticol[1] + 4*sumanticol[2] + 8*sumanticol[3] + 16*sumanticol[4]

        res = adv + dis
        
        self._squares[y][x]= 0
        return res

    def getBest_move(self,col = 2):
        '''
        trả lại điểm số của mảng trong lợi thế của từng màu
        '''
        if col == 2:
            anticol = 1
        else:
            anticol = 2
            
        movecol = (0,0)
        maxscorecol = 0
        # kiểm tra nếu bàn cờ rỗng thì cho vị trí random nếu không thì đưa ra giá trị trên bàn cờ nên đi 
        if self.isEmpty():
            movecol = ( int((self.board_row)*random.random()),int((self.board_row)*random.random()))
        else:
            moves = self.possible_moves()

            for move in moves:
                y,x = move
                if maxscorecol == 0:
                    scorecol=self.stupid_score(col,anticol,y,x)
                    maxscorecol = scorecol
                    movecol = move
                else:
                    scorecol=self.stupid_score(col,anticol,y,x)
                    if scorecol > maxscorecol:
                        maxscorecol = scorecol
                        movecol = move
        return movecol