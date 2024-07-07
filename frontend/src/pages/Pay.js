import React, { useState, useEffect } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import Header from "./Header";
import './Pay.css';

function Pay() {
  const [searchParams] = useSearchParams();
  const [whereToEat, setWhereToEat] = useState('');
  const [orderMenu, setOrderMenu] = useState('');
  const id = searchParams.get('id');
  const navigate = useNavigate();

  const fetchId = async () => {
    fetch('http://127.0.0.1:5000/api/getinfo/' + id)
    .then(response => response.json())
    .then(data => {
      setWhereToEat(data.wheretoeat);
    });
  };

  const cancel = () => {
      navigate('/howtopay?id=' + id);
  };
  
  const fetchOrderMenu = async () => {
    fetch('http://127.0.0.1:5000/api/ordermenu/' + id)
    .then(response => response.json())
    .then(data => {
        setOrderMenu(data);
    });
  };

  const pay = () => {
    fetch('http://127.0.0.1:5000/api/pay/' + id, {method: 'POST'})
    .then(navigate('/receipt?id=' + id));
  };

  useEffect(() => {
    fetchId();
    fetchOrderMenu();
  }, []);

  return (
    <>
      <Header whereToEat={whereToEat}/>
      <div className="orderList">
        <p className="titleOrderList">주문 내역</p>
        <div className="orderMenuList">
          <div className="orderMenuNameList">
            <div className="titleOrder">음식 이름</div>
            {orderMenu && orderMenu.map((menu, index) => {
              return (
                <div key={index} className="orderMenuName">
                  {menu.name}
                </div>
              )
            })}
          </div>
          <div className="orderMenuUnitPriceList">
            <div className="titleOrder">단가</div>
            {orderMenu && orderMenu.map((menu, index) => {
              return (
                <div key={index} className="orderMenuAmount">
                  {menu.price}
                </div>
              )
            })}
            </div>
            <div className="orderMenuAmountList">
              <div className="titleOrder">수량</div>
              {orderMenu && orderMenu.map((menu, index) => {
                return (
                  <div key={index} className="orderMenuAmount">
                    {menu.amount}
                  </div>
                )
              })}
          </div>
          <div className="orderMenuPriceList">
            <div className="titleOrder">가격</div>
            {orderMenu && orderMenu.map((menu, index) => {
              return (
                <div key={index} className="orderMenuPrice">
                  {menu.price * menu.amount}
                </div>
              )
            })}
          </div>
        </div>
        <hr className="orderLine" />
        <div className="totalPriceDiv">
            <div className="totalPriceTitle">총 가격</div>
            <div className="totalPrice">
                {orderMenu && orderMenu.reduce((acc, cur) => {
                    return acc + cur.price * cur.amount;
                }, 0)}원
            </div>
        </div>
      </div>
      <div className="cardInsertInfoDiv">
        <p className="cardInsertInfo">카드 단말기에</p>
        <p className="cardInsertInfo">카드를 넣어주세요.</p>
        <p className="cardReaderInfo">카드 단말기는 오른쪽 아래에 위치합니다.</p>
      </div>
      <button className="payCardButton" onClick={() => {pay()}}>결제하기</button>
      <footer className='footer3'>
        <button className='cancelButton3' onClick={() => {cancel()}}>이전으로</button>
      </footer>
    </>
  )
}

export default Pay;