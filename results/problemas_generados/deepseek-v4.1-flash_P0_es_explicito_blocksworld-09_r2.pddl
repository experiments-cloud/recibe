(define (problem blocks-9)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
    h - block
    i - block
  )
  (:init
    (ontable b)
    (ontable c)
    (on a i)
    (on d h)
    (on e a)
    (on f g)
    (on g e)
    (on h b)
    (on i d)
    (clear c)
    (clear f)
    (handempty)
  )
  (:goal
    (and
      (on a i)
      (on b c)
      (on c a)
      (on d b)
      (on e h)
      (on f e)
      (on g d)
      (on i f)
    )
  )
)
